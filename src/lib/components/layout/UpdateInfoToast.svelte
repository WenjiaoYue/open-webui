<script lang="ts">
	import { getContext, createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();
	const i18n = getContext('i18n');

	import { WEBUI_VERSION } from '$lib/constants';
	import XMark from '../icons/XMark.svelte';

</script>

<div
	class="flex items-start 
	bg-red-50 border border-red-500 text-red-600 placeholder-red-700 text-sm rounded-lg focus:ring-red-500 dark:bg-gray-700 focus:border-red-500 block w-full p-2.5 dark:text-red-500 dark:placeholder-red-500 dark:border-red-500
	 px-3.5 py-3 text-xs max-w-80 pr-2 w-full shadow-lg
	"
>
	<div class="flex-1 font-medium">
		<p class="font-bold">{$i18n.t(`NOTE`)}:</p>
		<p>{$i18n.t(`The backend will record all user's queries for debug purpose. `)}		
		</p>	
		<p>{$i18n.t(`please don't enter the sensitive or personal info during query.`)}</p>
	</div>

	<div class=" flex-shrink-0 pr-1">
		<button
			class=" hover:text-blue-900 dark:hover:text-blue-300 transition"
			on:click={() => {
				dispatch('close');
			}}
		>
			<XMark />
		</button>
	</div>
</div>
