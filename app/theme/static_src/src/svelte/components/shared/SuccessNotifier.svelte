<script>
  import { fly, scale, fade } from "svelte/transition";
  import UIStore from "../../store/ui";

  export let text = "Updated profile successfully";

  $: UIData = $UIStore;
</script>

{#if UIData.success}
  <div
    in:fly={{ y: 400, duration: 400 }}
    out:scale={{ start: 1.25 }}
    class="w-64 py-8 mt-6 ml-10 text-center absolute z-40 bg-black rounded-full
    sm:w-1/2 sm:py-10 sm:ml-16">
    <p class="text-white inline-block text-sm sm:text-base">{text}</p>
    <button
      on:click={() => UIStore.setSuccess(false)}
      class="w-8 h-8 text-white absolute right-0 top-0 mb-2 bg-indigo-600
      rounded-full">
      x
    </button>
  </div>
{/if}
