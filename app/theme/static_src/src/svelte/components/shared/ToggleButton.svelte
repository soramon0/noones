<script lang="ts">
  export let toggle: boolean = false;
</script>

<div
  on:click={() => (toggle = !toggle)}
  class="p-1 w-16 h-8 shadow-sm rounded-full bg-indigo-500 cursor-pointer">
  <button
    class="inline-block w-1/2 h-full rounded-full bg-white border border-white
    shadow-sm transform transition-transform duration-500 ease-out
    focus:outline-none {toggle ? 'translate-x-full' : 'translate-x-0 '}" />
</div>
