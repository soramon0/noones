<script>
  import { createEventDispatcher } from "svelte";

  export let text = "Update";

  const dispatch = createEventDispatcher();

  const forwardClick = () => dispatch("click");
</script>

<div class="text-right mt-6">
	<button on:click={forwardClick} class="btn-black hover:bg-gray-700 sm:w-auto">{text}</button>
</div>
