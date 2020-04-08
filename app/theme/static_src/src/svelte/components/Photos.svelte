<script>
  import { scale, fade } from "svelte/transition";
  import Breadcrumb from "./shared/Breadcrumb";
  import SaveButton from "./shared/SaveButton";
  import CancelButton from "./shared/CancelButton";

  export let photos;
  export let profile;
  export let cover;
  let showUploadModal = false;
  let showConfirmPictureUpload = false;

  const toggleUploadModal = () => (showUploadModal = !showUploadModal);
  const toggleConfirmPictureUpload = () =>
    (showConfirmPictureUpload = !showConfirmPictureUpload);
</script>

<style>
  @media (min-width: 640px) {
    .add-cover-container:hover .add-cover-text {
      opacity: 1;
    }

    .add-profile:hover .add-profile-container {
      transform: translateY(0);
    }
  }
</style>

<Breadcrumb activeText="Photos" />

{#if showUploadModal}
  <div
    transition:fade
    on:click={toggleUploadModal}
    class="fixed inset-0 bg-black z-20 opacity-50" />
  <div
    transition:scale={{ delay: 150 }}
    class="max-w-2xl w-4/5 h-500 overflow-y-scroll m-auto fixed inset-0 bg-white
    z-30 rounded-lg sm:1/2">
    <div class="text-center py-4 border-b-2 border-gray-200">
      <p class="font-semibold sm:text-2xl">Change your picture</p>
    </div>

    <div
      class="p-4 flex justify-evenly items-center bg-white border-b-2
      border-gray-200 ">
      <CancelButton on:click={toggleUploadModal} />

      <SaveButton text="Upload New Photo" />
    </div>

    <div class="p-4">
      <p class="text-lg font-semibold">From Gallery</p>
      <div class="mt-2 flex flex-wrap justify-evenly">
        <div
          on:click={toggleConfirmPictureUpload}
          class="h-32 w-32 bg-gray-300 cursor-pointer mb-2 border
          border-gray-300 hover:border-indigo-400" />
        <div
          class="h-32 w-32 bg-gray-300 cursor-pointer mb-2 border
          border-gray-300 hover:border-indigo-400" />
        <div
          class="h-32 w-32 bg-gray-300 cursor-pointer mb-2 border
          border-gray-300 hover:border-indigo-400" />
        <div
          class="h-32 w-32 bg-gray-300 cursor-pointer mb-2 border
          border-gray-300 hover:border-indigo-400" />
        <div
          class="h-32 w-32 bg-gray-300 cursor-pointer mb-2 border
          border-gray-300 hover:border-indigo-400" />
        <div
          class="h-32 w-32 bg-gray-300 cursor-pointer mb-2 border
          border-gray-300 hover:border-indigo-400" />
        <div
          class="h-32 w-32 bg-gray-300 cursor-pointer mb-2 border
          border-gray-300 hover:border-indigo-400" />
        <div
          class="h-32 w-32 bg-gray-300 cursor-pointer mb-2 border
          border-gray-300 hover:border-indigo-400" />
      </div>
      {#if showConfirmPictureUpload}
        <div
          transition:scale
          class="w-56 h-24 p-4 m-auto flex justify-evenly items-center fixed
          inset-0 bg-white z-40 rounded-lg shadow-md">
          <CancelButton on:click={toggleConfirmPictureUpload} />
          <SaveButton />
        </div>
      {/if}
    </div>
  </div>
{/if}

<div class="mt-4 pb-8 border-b border-gray-500">
  <div class="relative">
    <div
      on:click={toggleUploadModal}
      class="add-cover-container px-3 py-2 flex justify-evenly items-center
      absolute bottom-0 right-0 bg-gray-300 hover:bg-gray-300 cursor-pointer
      rounded-tl-md transition-colors duration-300 ease-out sm:bottom-auto
      sm:right-auto sm:top-0 sm:left-0 sm:ml-2 sm:mt-4 sm:bg-transparent
      sm:rounded">
      <svg class="w-6 h-6 sm:w-8 sm:h-8" viewBox="0 0 60 60">
        <g>
          <path
            d="M55.201,15.5h-8.524l-4-10H17.323l-4,10H12v-5H6v5H4.799C2.152,15.5,0,17.652,0,20.299v29.368
            C0,52.332,2.168,54.5,4.833,54.5h50.334c2.665,0,4.833-2.168,4.833-4.833V20.299C60,17.652,57.848,15.5,55.201,15.5z
            M8,12.5h2v3H8 V12.5z
            M58,49.667c0,1.563-1.271,2.833-2.833,2.833H4.833C3.271,52.5,2,51.229,2,49.667V20.299C2,18.756,3.256,17.5,4.799,17.5H6h6
            h2.677l4-10h22.646l4,10h9.878c1.543,0,2.799,1.256,2.799,2.799V49.667z" />
          <path
            d="M30,14.5c-9.925,0-18,8.075-18,18s8.075,18,18,18s18-8.075,18-18S39.925,14.5,30,14.5z
            M30,48.5c-8.822,0-16-7.178-16-16
            s7.178-16,16-16s16,7.178,16,16S38.822,48.5,30,48.5z" />
          <path
            d="M30,20.5c-6.617,0-12,5.383-12,12s5.383,12,12,12s12-5.383,12-12S36.617,20.5,30,20.5z
            M30,42.5c-5.514,0-10-4.486-10-10
            s4.486-10,10-10s10,4.486,10,10S35.514,42.5,30,42.5z" />
          <path
            d="M52,19.5c-2.206,0-4,1.794-4,4s1.794,4,4,4s4-1.794,4-4S54.206,19.5,52,19.5z
            M52,25.5c-1.103,0-2-0.897-2-2s0.897-2,2-2
            s2,0.897,2,2S53.103,25.5,52,25.5z" />
        </g>
        <g />
        <g />
        <g />
        <g />
        <g />
        <g />
        <g />
        <g />
        <g />
        <g />
        <g />
        <g />
        <g />
        <g />
        <g />
      </svg>

      <span
        class="add-cover-text transition-opacity duration-300 ease-out
        inline-block ml-2 sm:opacity-0">
        change cover
      </span>
    </div>

    <div
      class="w-full h-64 flex justify-center items-center bg-gray-200 rounded
      overflow-hidden">
      {#if cover}
        <img
          src={cover}
          alt="cover picture"
          class="w-full h-full object-cover" />
      {:else}
        <svg
          class="w-24 h-24"
          xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink"
          viewBox="0 0 415 415"
          style="enable-background:new 0 0 415 415;"
          xml:space="preserve">
          <g>
            <path
              d="M67.5,400H15v-52.5c0-4.143-3.358-7.5-7.5-7.5S0,343.357,0,347.5v60c0,4.143,3.358,7.5,7.5,7.5h60
              c4.142,0,7.5-3.357,7.5-7.5S71.642,400,67.5,400z" />
            <path
              d="M407.5,340c-4.142,0-7.5,3.357-7.5,7.5V400h-52.5c-4.142,0-7.5,3.357-7.5,7.5s3.358,7.5,7.5,7.5h60
              c4.142,0,7.5-3.357,7.5-7.5v-60C415,343.357,411.642,340,407.5,340z" />
            <path
              d="M67.5,0h-60C3.358,0,0,3.357,0,7.5v60C0,71.643,3.358,75,7.5,75s7.5-3.357,7.5-7.5V15h52.5c4.142,0,7.5-3.357,7.5-7.5
              S71.642,0,67.5,0z" />
            <path
              d="M407.5,0h-60c-4.142,0-7.5,3.357-7.5,7.5s3.358,7.5,7.5,7.5H400v52.5c0,4.143,3.358,7.5,7.5,7.5s7.5-3.357,7.5-7.5v-60
              C415,3.357,411.642,0,407.5,0z" />
            <path
              d="M267.5,200H215v-52.5c0-4.143-3.358-7.5-7.5-7.5s-7.5,3.357-7.5,7.5V200h-52.5c-4.142,0-7.5,3.357-7.5,7.5
              s3.358,7.5,7.5,7.5H200v52.5c0,4.143,3.358,7.5,7.5,7.5s7.5-3.357,7.5-7.5V215h52.5c4.142,0,7.5-3.357,7.5-7.5
              S271.642,200,267.5,200z" />
          </g>
          <g />
          <g />
          <g />
          <g />
          <g />
          <g />
          <g />
          <g />
          <g />
          <g />
          <g />
          <g />
          <g />
          <g />
          <g />
        </svg>
      {/if}
    </div>

    <div
      class="add-profile w-32 h-40 ml-4 -mb-4 absolute bottom-0 left-0
      bg-gray-200 rounded-md sm:overflow-hidden">
      <div class="rounded-md overflow-hidden">
        {#if profile}
          <img
            src={profile}
            alt="profile picture"
            class="w-full h-full object-cover" />
        {:else}
          <svg class="w-full h-full" viewBox="0 0 20 20">
            <path
              d="M10,10.9c2.373,0,4.303-1.932,4.303-4.306c0-2.372-1.93-4.302-4.303-4.302S5.696,4.223,5.696,6.594C5.696,8.969,7.627,10.9,10,10.9z
              M10,3.331c1.801,0,3.266,1.463,3.266,3.263c0,1.802-1.465,3.267-3.266,3.267c-1.8,0-3.265-1.465-3.265-3.267C6.735,4.794,8.2,3.331,10,3.331z" />
            <path
              d="M10,12.503c-4.418,0-7.878,2.058-7.878,4.685c0,0.288,0.231,0.52,0.52,0.52c0.287,0,0.519-0.231,0.519-0.52c0-1.976,3.132-3.646,6.84-3.646c3.707,0,6.838,1.671,6.838,3.646c0,0.288,0.234,0.52,0.521,0.52s0.52-0.231,0.52-0.52C17.879,14.561,14.418,12.503,10,12.503z" />
          </svg>
        {/if}
      </div>

      <div
        on:click={toggleUploadModal}
        class="add-profile-container h-10 w-10 absolute top-0 right-0 mt-2 -mr-4
        flex justify-center items-center bg-white rounded-full cursor-pointer
        sm:w-full sm:h-20 sm:top-auto sm:bottom-0 sm:bg-black sm:opacity-75
        sm:m-0 sm:rounded-bl-none sm:rounded-br-none sm:rounded-md
        sm:translate-y-full transform transition duration-300 ease-in-out">
        <svg
          class="w-4 h-4 fill-current text-black sm:text-white sm:w-10 sm:h-10"
          viewBox="0 0 60 60">
          <g>
            <path
              d="M55.201,15.5h-8.524l-4-10H17.323l-4,10H12v-5H6v5H4.799C2.152,15.5,0,17.652,0,20.299v29.368
              C0,52.332,2.168,54.5,4.833,54.5h50.334c2.665,0,4.833-2.168,4.833-4.833V20.299C60,17.652,57.848,15.5,55.201,15.5z
              M8,12.5h2v3H8 V12.5z
              M58,49.667c0,1.563-1.271,2.833-2.833,2.833H4.833C3.271,52.5,2,51.229,2,49.667V20.299C2,18.756,3.256,17.5,4.799,17.5H6h6
              h2.677l4-10h22.646l4,10h9.878c1.543,0,2.799,1.256,2.799,2.799V49.667z" />
            <path
              d="M30,14.5c-9.925,0-18,8.075-18,18s8.075,18,18,18s18-8.075,18-18S39.925,14.5,30,14.5z
              M30,48.5c-8.822,0-16-7.178-16-16
              s7.178-16,16-16s16,7.178,16,16S38.822,48.5,30,48.5z" />
            <path
              d="M30,20.5c-6.617,0-12,5.383-12,12s5.383,12,12,12s12-5.383,12-12S36.617,20.5,30,20.5z
              M30,42.5c-5.514,0-10-4.486-10-10
              s4.486-10,10-10s10,4.486,10,10S35.514,42.5,30,42.5z" />
            <path
              d="M52,19.5c-2.206,0-4,1.794-4,4s1.794,4,4,4s4-1.794,4-4S54.206,19.5,52,19.5z
              M52,25.5c-1.103,0-2-0.897-2-2s0.897-2,2-2
              s2,0.897,2,2S53.103,25.5,52,25.5z" />
          </g>
          <g />
          <g />
          <g />
          <g />
          <g />
          <g />
          <g />
          <g />
          <g />
          <g />
          <g />
          <g />
          <g />
          <g />
          <g />
          <svg
            class="w-8 h-8 "
            xmlns="http://www.w3.org/2000/svg"
            xmlns:xlink="http://www.w3.org/1999/xlink"
            viewBox="0 0 415 415"
            style="enable-background:new 0 0 415 415;"
            xml:space="preserve">
            <g>
              <path
                d="M67.5,400H15v-52.5c0-4.143-3.358-7.5-7.5-7.5S0,343.357,0,347.5v60c0,4.143,3.358,7.5,7.5,7.5h60
                c4.142,0,7.5-3.357,7.5-7.5S71.642,400,67.5,400z" />
              <path
                d="M407.5,340c-4.142,0-7.5,3.357-7.5,7.5V400h-52.5c-4.142,0-7.5,3.357-7.5,7.5s3.358,7.5,7.5,7.5h60
                c4.142,0,7.5-3.357,7.5-7.5v-60C415,343.357,411.642,340,407.5,340z" />
              <path
                d="M67.5,0h-60C3.358,0,0,3.357,0,7.5v60C0,71.643,3.358,75,7.5,75s7.5-3.357,7.5-7.5V15h52.5c4.142,0,7.5-3.357,7.5-7.5
                S71.642,0,67.5,0z" />
              <path
                d="M407.5,0h-60c-4.142,0-7.5,3.357-7.5,7.5s3.358,7.5,7.5,7.5H400v52.5c0,4.143,3.358,7.5,7.5,7.5s7.5-3.357,7.5-7.5v-60
                C415,3.357,411.642,0,407.5,0z" />
              <path
                d="M267.5,200H215v-52.5c0-4.143-3.358-7.5-7.5-7.5s-7.5,3.357-7.5,7.5V200h-52.5c-4.142,0-7.5,3.357-7.5,7.5
                s3.358,7.5,7.5,7.5H200v52.5c0,4.143,3.358,7.5,7.5,7.5s7.5-3.357,7.5-7.5V215h52.5c4.142,0,7.5-3.357,7.5-7.5
                S271.642,200,267.5,200z" />
            </g>
            <g />
            <g />
            <g />
            <g />
            <g />
            <g />
            <g />
            <g />
            <g />
            <g />
            <g />
            <g />
            <g />
            <g />
            <g />
          </svg>
        </svg>
      </div>
    </div>
  </div>
</div>

<h1 class="text-2xl mt-4">Gallery</h1>
<div class="mt-4 flex flex-wrap">
  {#each photos as photo, i}
    <div
      class="h-40 w-40 bg-gray-300 cursor-pointer mb-2 mr-2 rounded-md
      overflow-hidden border-2 hover:border-indigo-400 transform hover:scale-105
      transition-all duration-200 ease-out">
      <img
        src={photo.image}
        class="w-full h-full object-cover"
        alt="user image {i}" />
    </div>
  {:else}
    <p>No pictures.</p>
  {/each}
</div>
