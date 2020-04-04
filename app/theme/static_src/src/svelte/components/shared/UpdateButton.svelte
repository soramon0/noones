<script>
  export let text = "Update";
  export let fetching;
</script>

<div class="text-right mt-6">
  <button
    on:click
    disabled={fetching}
    class="btn-black hover:bg-gray-500 sm:w-auto {fetching ? 'bg-gray-700 cursor-not-allowed' : ''}">
    {text}
  </button>
</div>
