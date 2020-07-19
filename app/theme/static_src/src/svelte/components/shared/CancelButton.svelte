<script>
  export let text = "Cancel";
  export let fetching;
</script>

<button
  type="button"
  disabled={fetching}
  on:click
  class="text-sm px-6 py-3 text-gray-700 hover:bg-gray-400 rounded-md
  sm:text-base {fetching ? 'bg-gray-600 cursor-not-allowed' : ''}">
  {text}
</button>
