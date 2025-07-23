<script lang="ts">
	import { toast } from 'svelte-sonner';
	import { user, config, WEBUI_NAME, PROJECT_IMG } from '$lib/stores';
	import {
		updateUserProfile,
		getSessionUser,
		getAdminConfig,
		updateAdminConfig
	} from '$lib/apis/auths';

	import { generateInitialsImage, canvasPixelTest } from '$lib/utils';
	import { createEventDispatcher, onMount, getContext } from 'svelte';
	import { getBackendConfig } from '$lib/apis';

	const i18n = getContext('i18n');
	const dispatch = createEventDispatcher();

	let profileImageUrl =  $PROJECT_IMG;
	let name = $WEBUI_NAME;
	let adminConfig = {};

	let profileImageInputElement: HTMLInputElement;

	const submitHandler = async () => {
		if (name !== $user?.name) {
			if (profileImageUrl === generateInitialsImage($user?.name) || profileImageUrl === '') {
				profileImageUrl = generateInitialsImage(name);
			}
		}

		const updatedUser = await updateUserProfile(localStorage.token, name, profileImageUrl).catch(
			(error) => {
				toast.error(`${error}`);
			}
		);

		if (updatedUser) {
			// Get Session User Info
			const sessionUser = await getSessionUser(localStorage.token).catch((error) => {
				toast.error(`${error}`);
				return null;
			});

			await user.set(sessionUser);
			return true;
		}
		return false;
	};

	onMount(async () => {
		await Promise.all([
			(async () => {
				adminConfig = await getAdminConfig(localStorage.token);
				console.log('adminConfig', adminConfig);
			})()
		]);
	});

	const updateInterfaceHandler = async () => {
		// update adminConfig
		// 修改里面的adminConfig
		adminConfig.PROJECT_NAME = name;
		adminConfig.PROJECT_IMG_URL = profileImageUrl;

		const res = await updateAdminConfig(localStorage.token, adminConfig);
		console.log('admin update res', res);

		WEBUI_NAME.set(name);
		PROJECT_IMG.set(profileImageUrl);

		// update config --name + imgURL
		const backendConfig = await getBackendConfig();
		console.log('backendConfig', backendConfig);
		

	};
</script>

<form
	class="flex flex-col h-full justify-between space-y-3 text-sm"
	on:submit|preventDefault={() => {
		updateInterfaceHandler();
		dispatch('save');
	}}
>
	<div class="flex flex-col h-full justify-between text-sm">
		<div class=" space-y-3 overflow-y-scroll max-h-[28rem] lg:max-h-full">
			<input
				id="profile-image-input"
				bind:this={profileImageInputElement}
				type="file"
				hidden
				accept="image/*"
				on:change={(e) => {
					const files = profileImageInputElement.files ?? [];
					let reader = new FileReader();
					reader.onload = (event) => {
						let originalImageUrl = `${event.target.result}`;

						const img = new Image();
						img.src = originalImageUrl;

						img.onload = function () {
							const canvas = document.createElement('canvas');
							const ctx = canvas.getContext('2d');

							// Calculate the aspect ratio of the image
							const aspectRatio = img.width / img.height;

							// Calculate the new width and height to fit within 250x250
							let newWidth, newHeight;
							if (aspectRatio > 1) {
								newWidth = 250 * aspectRatio;
								newHeight = 250;
							} else {
								newWidth = 250;
								newHeight = 250 / aspectRatio;
							}

							// Set the canvas size
							canvas.width = 250;
							canvas.height = 250;

							// Calculate the position to center the image
							const offsetX = (250 - newWidth) / 2;
							const offsetY = (250 - newHeight) / 2;

							// Draw the image on the canvas
							ctx.drawImage(img, offsetX, offsetY, newWidth, newHeight);

							// Get the base64 representation of the compressed image
							const compressedSrc = canvas.toDataURL('image/jpeg');

							// Display the compressed image
							profileImageUrl = compressedSrc;

							profileImageInputElement.files = null;
						};
					};

					if (
						files.length > 0 &&
						['image/gif', 'image/webp', 'image/jpeg', 'image/png'].includes(files[0]['type'])
					) {
						reader.readAsDataURL(files[0]);
					}
				}}
			/>

			<div class="space-y-1">
				<div class="flex space-x-5">
					<div class="flex flex-col">
						<div class="self-center mt-2">
							<button
								class="relative rounded-full dark:bg-gray-700"
								type="button"
								on:click={() => {
									profileImageInputElement.click();
								}}
							>
								<img
									src={profileImageUrl !== '' ? profileImageUrl : generateInitialsImage(name)}
									alt="profile"
									class=" rounded-full size-16 object-cover"
								/>

								<div
									class="absolute flex justify-center rounded-full bottom-0 left-0 right-0 top-0 h-full w-full overflow-hidden bg-gray-700 bg-fixed opacity-0 transition duration-300 ease-in-out hover:opacity-50"
								>
									<div class="my-auto text-gray-100">
										<svg
											xmlns="http://www.w3.org/2000/svg"
											viewBox="0 0 20 20"
											fill="currentColor"
											class="w-5 h-5"
										>
											<path
												d="m2.695 14.762-1.262 3.155a.5.5 0 0 0 .65.65l3.155-1.262a4 4 0 0 0 1.343-.886L17.5 5.501a2.121 2.121 0 0 0-3-3L3.58 13.419a4 4 0 0 0-.885 1.343Z"
											/>
										</svg>
									</div>
								</div>
							</button>
						</div>
					</div>

					<div class="flex-1 flex flex-col self-center gap-0.5">
						<div class=" mb-0.5 text-sm font-medium">{$i18n.t('Project Image')}</div>

						<div>
							<button
								class=" text-xs text-center text-gray-800 dark:text-gray-400 rounded-full px-4 py-0.5 bg-gray-100 dark:bg-gray-850"
								on:click={async () => {
									if (canvasPixelTest()) {
										profileImageUrl = generateInitialsImage(name);
									} else {
										toast.info(
											$i18n.t(
												'Fingerprint spoofing detected: Unable to use initials as avatar. Defaulting to default profile image.'
											),
											{
												duration: 1000 * 10
											}
										);
									}
								}}>{$i18n.t('Use Initials')}</button
							>

							<button
								class=" text-xs text-center text-gray-800 dark:text-gray-400 rounded-lg px-2 py-1"
								on:click={async () => {
									profileImageUrl = '/user.png';
								}}>{$i18n.t('Remove')}</button
							>
						</div>
					</div>
				</div>

				<div class="pt-0.5">
					<div class="flex flex-col w-full">
						<div class=" mb-1 text-sm font-semibold">{$i18n.t('Project Name')}</div>

						<div class="flex-1">
							<input
								class="border-b border-gray-400 w-full py-2 text-sm dark:text-gray-300 dark:bg-gray-850 outline-hidden"
								type="text"
								bind:value={name}
								required
								placeholder={$i18n.t('Enter your name')}
							/>
						</div>
					</div>
				</div>
			</div>
		</div>

		<div class="flex justify-end pt-3 text-sm font-medium">
			<button
				class="px-3.5 py-1.5 text-sm font-medium bg-black hover:bg-gray-900 text-white dark:bg-white dark:text-black dark:hover:bg-gray-100 transition rounded-full"
			>
				{$i18n.t('Save')}
			</button>
		</div>
	</div>
</form>
