<script lang="ts">
  import { fly, scale, fade } from 'svelte/transition';
  import { UIStore } from '../../store/index';

  export let text = 'Updated profile successfully';

  $: UIData = $UIStore;
</script>

{#if UIData.showFeedbackModal}
  <div
    in:fly={{ y: 400, duration: 400 }}
    out:scale={{ start: 1.25 }}
    class="w-64 py-8 mt-6 ml-10 text-center absolute z-40 bg-black rounded-full
    sm:w-1/2 sm:py-10 sm:ml-16">
    <p class="text-white inline-block text-sm sm:text-base">{text}</p>
    <button
      on:click={() => UIStore.setFeedbackModal(false)}
      class="w-8 h-8 text-white absolute right-0 top-0 mb-2 bg-indigo-600
      rounded-full">
      <svg viewBox="0 0 20 20" class="w-full h-full fill-current text-white">
        <path
          d="M12.71,7.291c-0.15-0.15-0.393-0.15-0.542,0L10,9.458L7.833,7.291c-0.15-0.15-0.392-0.15-0.542,0c-0.149,0.149-0.149,0.392,0,0.541L9.458,10l-2.168,2.167c-0.149,0.15-0.149,0.393,0,0.542c0.15,0.149,0.392,0.149,0.542,0L10,10.542l2.168,2.167c0.149,0.149,0.392,0.149,0.542,0c0.148-0.149,0.148-0.392,0-0.542L10.542,10l2.168-2.168C12.858,7.683,12.858,7.44,12.71,7.291z
          M10,1.188c-4.867,0-8.812,3.946-8.812,8.812c0,4.867,3.945,8.812,8.812,8.812s8.812-3.945,8.812-8.812C18.812,5.133,14.867,1.188,10,1.188z
          M10,18.046c-4.444,0-8.046-3.603-8.046-8.046c0-4.444,3.603-8.046,8.046-8.046c4.443,0,8.046,3.602,8.046,8.046C18.046,14.443,14.443,18.046,10,18.046z" />
      </svg>
    </button>
  </div>
{/if}
