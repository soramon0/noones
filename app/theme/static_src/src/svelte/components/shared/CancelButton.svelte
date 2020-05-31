<script>
  export let text = "Cancel";
  export let fetching;
</script>

<button
  type="button"
  disabled={fetching}
  on:click
  class="px-6 py-3 hover:bg-gray-400 rounded-md {fetching ? 'bg-gray-600 cursor-not-allowed' : ''}">
  {text}
</button>
