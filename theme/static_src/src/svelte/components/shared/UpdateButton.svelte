<script lang="ts">
  export let text = 'Update';
  export let fetching: boolean;
  export let type = 'submit';
</script>

<button
  {type}
  on:click
  disabled={fetching}
  class="w-full px-8 py-3 text-xs rounded-md tracking-wider bg-black text-white
  hover:bg-gray-900 transition-transform duration-200 ease-in-out transform
  hover:scale-110 sm:w-auto sm:text-sm md:text-base {fetching ? 'bg-gray-700 cursor-not-allowed' : ''}">
  {text}
</button>
