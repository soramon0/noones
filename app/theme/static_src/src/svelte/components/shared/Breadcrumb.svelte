<script lang="ts">
  export let activeText: string;
  export let text = 'Edit Profile';
</script>

<div class="ml-4 py-3 sm:ml-0">
  <div
    class="px-3 ml-3 border-l border-gray-600 flex items-center sm:ml-0
    sm:border-0">
    <span class="text-xs text-gray-600 sm:text-base">{activeText}</span>
    <div class="mx-1 flex items-center">
      <svg class="h-3 w-3 fill-current text-400" viewBox="0 0 20 20">
        <path
          d="M11.611,10.049l-4.76-4.873c-0.303-0.31-0.297-0.804,0.012-1.105c0.309-0.304,0.803-0.293,1.105,0.012l5.306,5.433c0.304,0.31,0.296,0.805-0.012,1.105L7.83,15.928c-0.152,0.148-0.35,0.223-0.547,0.223c-0.203,0-0.406-0.08-0.559-0.236c-0.303-0.309-0.295-0.803,0.012-1.104L11.611,10.049z" />
      </svg>
    </div>
    <span class="text-xs text-gray-800 sm:text-base">{text}</span>
  </div>
</div>
