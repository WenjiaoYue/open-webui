<script lang="ts">
	export let token;
	export let onClick: Function = () => {};

	let attributes: Record<string, string> | string = {};

	function extractAttributes(input: string): Record<string, string> | string {
		console.log('extractAttributes', input, typeof(input));
		
		const regex = /(\w+)="([^"]*)"/g;
		let match;
		let attrs: Record<string, string> = {};

		// Loop through all matches and populate the attributes object
		while ((match = regex.exec(input)) !== null) {
			attrs[match[1]] = match[2];
		}

		if (Object.keys(attrs).length === 0) {
			return input;
		}
		console.log('attrs', attrs);
		
		return attrs;
	}

	$: attributes = extractAttributes(token.text);
</script>

{#if typeof attributes !== 'string' && attributes.title}
	<button
		class="text-xs font-medium w-fit translate-y-[2px] px-2 py-0.5 dark:bg-white/5 dark:text-white/60 dark:hover:text-white bg-gray-50 text-black/60 hover:text-black transition rounded-lg"
		on:click={() => {
			onClick(attributes.data);
		}}
	>
		<span class="line-clamp-1">
			{attributes.title}
		</span>
	</button>
{:else}
	<span>
		{attributes}
	</span>
{/if}
