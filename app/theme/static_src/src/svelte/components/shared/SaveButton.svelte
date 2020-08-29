<script lang="ts">
  export let text = 'Save';
  export let fetching: boolean;
</script>

<button
  on:click
  disabled={fetching}
  class="px-4 py-3 text-sm rounded-md tracking-wider bg-indigo-600 text-white
  hover:bg-indigo-700 transition-transform duration-200 ease-in-out transform
  hover:scale-110 sm:text-base">
  {text}
</button>
