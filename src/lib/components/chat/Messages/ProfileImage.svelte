<script lang="ts">
	import { WEBUI_BASE_URL } from '$lib/constants';
	import { PROJECT_IMG } from '$lib/stores';

	export let className = 'size-8';
</script>

<img
	crossorigin="anonymous"
	src={$PROJECT_IMG}
	class=" {className} object-cover rounded-full -translate-y-[1px]"
	alt="profile"
	draggable="false"
/>
