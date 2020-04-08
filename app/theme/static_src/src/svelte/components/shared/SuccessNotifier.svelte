<script>
  import { fly, scale, fade } from "svelte/transition";

  export let response;
  export let text = "Updated profile successfully";
</script>

{#if response}
  <div
    in:fly={{ y: 400, duration: 400 }}
    out:scale={{ start: 1.25 }}
    class="w-64 py-8 mt-6 ml-10 text-center absolute bg-black rounded-full
    sm:w-1/2 sm:py-10 sm:ml-16">
    <p class="text-white text-sm sm:text-base">{text}</p>
  </div>
{/if}
