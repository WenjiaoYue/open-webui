<script lang="ts">
	import { getContext, onMount } from 'svelte';
	import { toast } from 'svelte-sonner';

	import {
		WEBUI_NAME,
		chatId,
		mobile,
		settings,
		showArchivedChats,
		showControls,
		showSidebar,
		temporaryChatEnabled,
		user
	} from '$lib/stores';

	import { slide } from 'svelte/transition';
	import { page } from '$app/stores';

	import ShareChatModal from '../chat/ShareChatModal.svelte';
	import ModelSelector from '../chat/ModelSelector.svelte';
	import Tooltip from '../common/Tooltip.svelte';
	import Menu from '$lib/components/layout/Navbar/Menu.svelte';
	import UserMenu from '$lib/components/layout/Sidebar/UserMenu.svelte';
	import MenuLines from '../icons/MenuLines.svelte';
	import AdjustmentsHorizontal from '../icons/AdjustmentsHorizontal.svelte';

	import PencilSquare from '../icons/PencilSquare.svelte';

	import PerfMonitor from '../icons/PerfMonitor.svelte';
	import ZhTransEn from '../icons/zhTransEn.svelte';
	import { userSignOut } from '$lib/apis/auths';
	import EnTransZh from '../icons/EnTransZh.svelte';
	import { changeLanguage } from '$lib/i18n';

	const i18n = getContext('i18n');

	export let initNewChat: Function;
	export let title: string = $WEBUI_NAME;
	export let shareEnabled: boolean = false;

	export let chat;
	export let selectedModels;
	export let showModelSelector = true;

	let showShareChatModal = false;
	let showDownloadChatModal = false;

	let modelMapLinks = {
		'emr./models/DeepSeek-R1-Channel-INT8':
			'http://10.165.58.224:3000/d/sglang-dashboard-0416/sglang?orgId=1&refresh=5s&var-instance=beiy85ifk1hq8d&var-model_name=%2Fmodels%2FDeepSeek-R1-Channel-INT8',
		'gnr./models/DeepSeek-R1-Channel-INT8':
			'http://10.165.58.224:3000/d/sglang-dashboard-0416/sglang?orgId=1&refresh=5s&var-instance=eeiy820gtdjb4a&var-model_name=%2Fmodels%2FDeepSeek-R1-Channel-INT8',
		'deepseek-ai/DeepSeek-R1-Distill-Qwen-14B': '',
		'deepseek-ai/DeepSeek-R1-Distill-Qwen-32B': '',
		'/data/DeepSeek-R1-BF16-w8afp8-static-no-ste-G2':
			'http://10.165.58.224:3000/d/b281712d-8bff-41ef-9f3f-71ad43c05e9fxd/vllm?orgId=1&var-DS_PROMETHEUS=default&var-model_name=',
		'/models/qwq-32b-q8_0-00001-of-00009.gguf':
			'http://10.165.58.224:3000/d/cee0geqo7uigwc/llamacpp?orgId=1'
	};

	const switchLanguage = async () => {
		if ($i18n.language === 'zh-CN') {
			changeLanguage('en-US');
		} else {
			changeLanguage('zh-CN');
		}
	};
</script>

<ShareChatModal bind:show={showShareChatModal} chatId={$chatId} />

<nav class="sticky top-0 z-30 w-full px-1.5 py-1.5 -mb-8 flex items-center drag-region">
	<div
		class=" bg-gradient-to-b via-50% from-white via-white to-transparent dark:from-gray-900 dark:via-gray-900 dark:to-transparent pointer-events-none absolute inset-0 -bottom-7 z-[-1] blur"
	></div>

	<div class=" flex max-w-full w-full mx-auto px-1 pt-0.5 bg-transparent">
		<div class="flex items-center w-full max-w-full">
			{#if $user.name !== 'Guest'}
				<div
					class="{$showSidebar
						? 'md:hidden'
						: ''} mr-1 self-start flex flex-none items-center text-gray-600 dark:text-gray-400"
				>
					<button
						id="sidebar-toggle-button"
						class="cursor-pointer px-2 py-2 flex rounded-xl hover:bg-gray-50 dark:hover:bg-gray-850 transition"
						on:click={() => {
							showSidebar.set(!$showSidebar);
						}}
						aria-label="Toggle Sidebar"
					>
						<div class=" m-auto self-center">
							<MenuLines />
						</div>
					</button>
				</div>
			{/if}

			<div
				class="flex-1 overflow-hidden max-w-full py-0.5
			{$showSidebar ? 'ml-1' : ''}
			"
			>
				{#if showModelSelector}
					<ModelSelector bind:selectedModels showSetDefault={!shareEnabled} />
				{/if}
			</div>
			<div class="self-start flex flex-none items-start text-gray-600 dark:text-gray-400">
				<!-- <div class="md:hidden flex self-center w-[1px] h-5 mx-2 bg-gray-300 dark:bg-stone-700" /> -->
				<Tooltip content={$i18n.t('Grafana')}>
					<a
						href={modelMapLinks[selectedModels] || '#'}
						aria-label="Grafana"
						target="_blank"
						rel="noopener noreferrer"
						class="flex cursor-pointer px-2 py-2 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-850 transition relative flex items-center justify-center cursor-pointer px-2 py-2 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-850 transition"
					>
						<div class=" flex flex-col items-center gap-1">
							<!-- <PerfMonitor className="size-5" strokeWidth="2" /> -->
							<p class="absolute text-[0.6rem] text-center -bottom-2">Grafana</p>
						</div>
					</a>
				</Tooltip>
				<Tooltip content={$i18n.t('Lang')}>
					<button
						class="
						flex cursor-pointer px-2 py-1 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-850 transition
							"
						on:click={(e) => {
							switchLanguage();
						}}
					>
						{#if $i18n.language === 'zh-CN'}
							<ZhTransEn className="size-7" strokeWidth="5" />
						{:else}
							<EnTransZh className="size-7" strokeWidth="5" />
						{/if}
					</button>
				</Tooltip>
				{#if shareEnabled && chat && (chat.id || $temporaryChatEnabled)}
					<Menu
						{chat}
						{shareEnabled}
						shareHandler={() => {
							showShareChatModal = !showShareChatModal;
						}}
						downloadHandler={() => {
							showDownloadChatModal = !showDownloadChatModal;
						}}
					>
						<button
							class="flex cursor-pointer px-2 py-2 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-850 transition"
							id="chat-context-menu-button"
						>
							<div class=" m-auto self-center">
								<svg
									xmlns="http://www.w3.org/2000/svg"
									fill="none"
									viewBox="0 0 24 24"
									stroke-width="1.5"
									stroke="currentColor"
									class="size-5"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										d="M6.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM12.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM18.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z"
									/>
								</svg>
							</div>
						</button>
					</Menu>
				{:else if $mobile && ($user.role === 'admin' || $user?.permissions?.chat?.controls)}
					<Tooltip content={$i18n.t('Controls')}>
						<button
							class=" flex cursor-pointer px-2 py-2 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-850 transition"
							on:click={async () => {
								await showControls.set(!$showControls);
							}}
							aria-label="Controls"
						>
							<div class=" m-auto self-center">
								<AdjustmentsHorizontal className=" size-5" strokeWidth="0.5" />
							</div>
						</button>
					</Tooltip>
				{/if}

				{#if $user.name === 'Guest'}
					<button
						class="flex py-2 px-3 w-full bg-[#1662c7] text-white hover:bg-gray-500 dark:hover:bg-gray-800 transition"
						on:click={async () => {
							await userSignOut();
							localStorage.removeItem('token');
							location.href = '/auth';
						}}
					>
						signin
					</button>
				{:else}
					{#if !$mobile && ($user.role === 'admin' || $user?.permissions?.chat?.controls)}
						<Tooltip content={$i18n.t('Controls')}>
							<button
								class=" flex cursor-pointer px-2 py-2 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-850 transition"
								on:click={async () => {
									await showControls.set(!$showControls);
								}}
								aria-label="Controls"
							>
								<div class=" m-auto self-center">
									<AdjustmentsHorizontal className=" size-5" strokeWidth="0.5" />
								</div>
							</button>
						</Tooltip>
					{/if}

					<Tooltip content={$i18n.t('New Chat')}>
						<button
							id="new-chat-button"
							class=" flex {$showSidebar
								? 'md:hidden'
								: ''} cursor-pointer px-2 py-2 rounded-xl text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-850 transition"
							on:click={() => {
								initNewChat();
							}}
							aria-label="New Chat"
						>
							<div class=" m-auto self-center">
								<PencilSquare className=" size-5" strokeWidth="2" />
							</div>
						</button>
					</Tooltip>

					{#if $user !== undefined}
						<UserMenu
							className="max-w-[200px]"
							role={$user.role}
							on:show={(e) => {
								if (e.detail === 'archived-chat') {
									showArchivedChats.set(true);
								}
							}}
						>
							<button
								class="select-none flex rounded-xl p-1.5 w-full hover:bg-gray-50 dark:hover:bg-gray-850 transition"
								aria-label="User Menu"
							>
								<div class=" self-center">
									<img
										src={$user.profile_image_url}
										class="size-6 object-cover rounded-full"
										alt="User profile"
										draggable="false"
									/>
								</div>
							</button>
						</UserMenu>
					{/if}
				{/if}
			</div>
		</div>
	</div>
</nav>
