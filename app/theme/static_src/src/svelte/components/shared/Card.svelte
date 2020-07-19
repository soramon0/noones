<script>
  export let classes = "";
  export let title = "";
  export let description = "";
</script>

<div class="py-4 px-6 mt-4 border w-full bg-white shadow rounded-lg {classes}">
  {#if title}
    <h3 class="mt-4 mb-2 text-lg font-semibold text-gray-700 sm:text-2xl">
      {title}
    </h3>
  {/if}
  {#if description}
    <p class="text-sm text-gray-600 mb-2 sm:text-base">{description}</p>
  {/if}
  <slot />
</div>
