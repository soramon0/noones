<script>
  import { createEventDispatcher } from "svelte";

  export let text = "Cancel";

  const dispatch = createEventDispatcher();

  const forwardClick = () => dispatch("click");
</script>

<button on:click={forwardClick} class="px-6 py-3 hover:bg-gray-400 rounded-md">
  {text}
</button>
