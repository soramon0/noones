<script>
  import { PhotoStore } from '../store/photo';

  // TODO(karim): change this if i reuse this component
  export const id = '';

  // Subscribe to the store
  $: photoData = $PhotoStore;
</script>

<div
  class="py-6 mb-2 flex items-center justify-center border-b-2 border-gray-300">
  <div
    class="w-12 h-12 border border-gray-500 rounded-full overflow-hidden md:w-16
    md:h-16">
    {#if photoData.profile}
      <img
        src={photoData.profile}
        alt="user profile"
        class="h-full w-full object-cover" />
    {:else}
      <svg class="fill-current text-gray-700 w-full h-full" viewBox="0 0 20 20">
        <path
          d="M10,10.9c2.373,0,4.303-1.932,4.303-4.306c0-2.372-1.93-4.302-4.303-4.302S5.696,4.223,5.696,6.594C5.696,8.969,7.627,10.9,10,10.9z
          M10,3.331c1.801,0,3.266,1.463,3.266,3.263c0,1.802-1.465,3.267-3.266,3.267c-1.8,0-3.265-1.465-3.265-3.267C6.735,4.794,8.2,3.331,10,3.331z" />
        <path
          d="M10,12.503c-4.418,0-7.878,2.058-7.878,4.685c0,0.288,0.231,0.52,0.52,0.52c0.287,0,0.519-0.231,0.519-0.52c0-1.976,3.132-3.646,6.84-3.646c3.707,0,6.838,1.671,6.838,3.646c0,0.288,0.234,0.52,0.521,0.52s0.52-0.231,0.52-0.52C17.879,14.561,14.418,12.503,10,12.503z" />
      </svg>
    {/if}
  </div>
  <!-- <a
    href={`/models/${id}`}
    class="ml-2 text-base text-gray-700 tracking-wide font-semibold sm:hidden
    md:block md:text-lg">
    My Page
  </a> -->
</div>
