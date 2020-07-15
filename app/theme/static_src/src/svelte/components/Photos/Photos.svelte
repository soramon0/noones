<script>
  import { onMount } from "svelte";
  import { fade } from "svelte/transition";
  import PhotoStore from "../../store/photo";
  import UIStore from "../../store/ui";
  import UpdatesStore from "../../store/updates";
  import SaveButton from "../shared/SaveButton";
  import TabView from "../shared/TabView";
  import SuccessNotifier from "../shared/SuccessNotifier";
  import ErrorNotifier from "../shared/ErrorNotifier";
  import UploadModal from "../shared/UploadModal";
  import ChangeGalleryPicture from "./ChangeGalleryPicture";
  import PhotoUpdateCard from "./PhotoUpdateCard";
  import ProfilePicturesTab from "./ProfilePicturesTab";
  import CoverPicturesTab from "./CoverPicturesTab";

  export let profilePicture;
  export let coverPicture;

  let selectedGalleryImage = 0;
  let showProfileModal = false;
  let showGalleryModal = false;
  let showCoverModal = false;
  let tabs = [
    { name: "All" },
    { name: "Profile Pictures" },
    { name: "Cover Pictures" },
    { name: "Gallery" }
  ];
  let tabName = tabs[0].name;

  // Subscribe to the store
  $: photoData = $PhotoStore;
  $: uiData = $UIStore;
  $: updatesData = $UpdatesStore;

  const setSelectedGalleryImage = index => {
    selectedGalleryImage = index;
  };

  const onShowProfileModal = () => {
    showProfileModal = !showProfileModal;
  };
  const onShowGalleryModal = () => {
    showGalleryModal = !showGalleryModal;
  };
  const onShowCoverModal = () => {
    showCoverModal = !showCoverModal;
  };

  onMount(() => {
    // Get user gallery updates
    if (!updatesData.gallery.length) {
      UpdatesStore.getGalleryUpdate();
    }

    if (!updatesData.coverPictures.length) {
      UpdatesStore.getCoverPictureUpdate();
    }

    if (!updatesData.profilePictures.length) {
      UpdatesStore.getProfilePicturesUpdate();
    }

    if (!photoData.profile.data.length) {
      PhotoStore.getProfilePictures();
    }

    if (!photoData.cover.data.length) {
      PhotoStore.getCoverPictures();
    }
  });

  $: console.log(photoData);
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

{#if showCoverModal}
  <UploadModal
    title="Upload a cover picture"
    errorKey="coverPicture"
    on:show={onShowCoverModal}
    on:file={({ detail }) => UpdatesStore.createCoverPictureUpdate(detail)}
    {photoData}
    {uiData} />
{:else if showProfileModal}
  <UploadModal
    title="Upload a Profile picture"
    errorKey="profilePicture"
    on:show={onShowProfileModal}
    on:file={({ detail }) => UpdatesStore.createProfilePictureUpdate(detail)}
    {photoData}
    {uiData} />
{:else if showGalleryModal}
  <UploadModal
    title="Gallery Images"
    errorKey="gallery"
    multiple
    on:show={onShowGalleryModal}
    on:file={({ detail }) => UpdatesStore.createGallaryPhotoUpdate(detail)}
    {photoData}
    {uiData} />
{/if}

<SuccessNotifier />
<TabView {tabs} {tabName} on:change={({ detail }) => (tabName = detail)}>
  {#if tabName === tabs[0].name}
    <div transition:fade={{ duration: 400 }} class="mt-4 pb-8">
      <div class="border-b">
        <div class="relative">
          <!-- Cover picture section -->
          <div
            on:click={onShowCoverModal}
            class="add-cover-container px-3 py-2 flex justify-evenly
            items-center absolute bottom-0 right-0 bg-gray-300 hover:bg-gray-300
            cursor-pointer rounded-tl-md transition-colors duration-300 ease-out
            sm:bottom-auto sm:right-auto sm:top-0 sm:left-0 sm:ml-2 sm:mt-4
            sm:bg-transparent sm:rounded">
            <svg
              class="w-6 h-6 fill-current text-gray-600 sm:w-8 sm:h-8"
              viewBox="0 0 20 20">
              <path
                d="M9.999,8.472c-1.314,0-2.385,1.069-2.385,2.384c0,1.317,1.07,2.385,2.385,2.385c1.316,0,2.386-1.068,2.386-2.385C12.385,9.541,11.314,8.472,9.999,8.472z
                M9.999,12.238c-0.76,0-1.38-0.622-1.38-1.382c0-0.761,0.62-1.38,1.38-1.38c0.761,0,1.38,0.62,1.38,1.38C11.379,11.616,10.76,12.238,9.999,12.238z" />
              <path
                d="M15.232,5.375H9.398C9.159,4.366,8.247,3.61,7.174,3.61c-1.073,0-1.985,0.756-2.224,1.765H4.769c-1.246,0-2.259,1.012-2.259,2.257v6.499c0,1.247,1.014,2.259,2.259,2.259h10.464c1.244,0,2.258-1.012,2.258-2.259V7.632C17.49,6.387,16.477,5.375,15.232,5.375z
                M16.486,14.131c0,0.69-0.564,1.256-1.254,1.256H4.769c-0.692,0-1.256-0.565-1.256-1.256V7.632c0-0.691,0.563-1.254,1.256-1.254H5.39c0.275,0,0.499-0.221,0.502-0.495c0.01-0.7,0.585-1.269,1.282-1.269s1.272,0.569,1.282,1.269c0.003,0.274,0.228,0.495,0.502,0.495h6.275c0.689,0,1.254,0.563,1.254,1.254V14.131z" />
            </svg>

            <span
              class="add-cover-text transition-opacity duration-300 ease-out
              inline-block ml-2 sm:opacity-0">
              change cover
            </span>
          </div>

          <div
            class="w-full h-64 flex justify-center items-center bg-gray-200
            rounded overflow-hidden">
            {#if coverPicture.image}
              <img
                alt="model cover"
                src={coverPicture.image}
                class="w-full h-full object-cover" />
            {:else}
              <svg
                class="w-12 h-12 fill-current text-gray-500 cursor-pointer"
                viewBox="0 0 20 20"
                on:click={onShowCoverModal}>
                <path
                  d="M8.416,3.943l1.12-1.12v9.031c0,0.257,0.208,0.464,0.464,0.464c0.256,0,0.464-0.207,0.464-0.464V2.823l1.12,1.12c0.182,0.182,0.476,0.182,0.656,0c0.182-0.181,0.182-0.475,0-0.656l-1.744-1.745c-0.018-0.081-0.048-0.16-0.112-0.224C10.279,1.214,10.137,1.177,10,1.194c-0.137-0.017-0.279,0.02-0.384,0.125C9.551,1.384,9.518,1.465,9.499,1.548L7.76,3.288c-0.182,0.181-0.182,0.475,0,0.656C7.941,4.125,8.234,4.125,8.416,3.943z
                  M15.569,6.286h-2.32v0.928h2.32c0.512,0,0.928,0.416,0.928,0.928v8.817c0,0.513-0.416,0.929-0.928,0.929H4.432c-0.513,0-0.928-0.416-0.928-0.929V8.142c0-0.513,0.416-0.928,0.928-0.928h2.32V6.286h-2.32c-1.025,0-1.856,0.831-1.856,1.856v8.817c0,1.025,0.832,1.856,1.856,1.856h11.138c1.024,0,1.855-0.831,1.855-1.856V8.142C17.425,7.117,16.594,6.286,15.569,6.286z" />
              </svg>
            {/if}
          </div>

          <!-- Profile picture section -->
          <div
            class="add-profile w-32 h-40 ml-4 -mb-4 absolute bottom-0 left-0
            bg-gray-200 rounded-md sm:overflow-hidden">
            <div class="rounded-md overflow-hidden">
              {#if profilePicture.image}
                <img
                  src={profilePicture.image}
                  alt="model profile"
                  class="w-full h-full object-cover" />
              {:else}
                <svg
                  class="w-full h-full fill-current text-gray-600"
                  viewBox="0 0 20 20">
                  <path
                    d="M10,10.9c2.373,0,4.303-1.932,4.303-4.306c0-2.372-1.93-4.302-4.303-4.302S5.696,4.223,5.696,6.594C5.696,8.969,7.627,10.9,10,10.9z
                    M10,3.331c1.801,0,3.266,1.463,3.266,3.263c0,1.802-1.465,3.267-3.266,3.267c-1.8,0-3.265-1.465-3.265-3.267C6.735,4.794,8.2,3.331,10,3.331z" />
                  <path
                    d="M10,12.503c-4.418,0-7.878,2.058-7.878,4.685c0,0.288,0.231,0.52,0.52,0.52c0.287,0,0.519-0.231,0.519-0.52c0-1.976,3.132-3.646,6.84-3.646c3.707,0,6.838,1.671,6.838,3.646c0,0.288,0.234,0.52,0.521,0.52s0.52-0.231,0.52-0.52C17.879,14.561,14.418,12.503,10,12.503z" />
                </svg>
              {/if}
            </div>

            <div
              on:click={onShowProfileModal}
              class="add-profile-container h-10 w-10 absolute top-0 right-0 mt-2
              -mr-4 flex justify-center items-center bg-white rounded-full
              cursor-pointer sm:w-full sm:h-20 sm:top-auto sm:bottom-0
              sm:bg-black sm:opacity-75 sm:m-0 sm:rounded-bl-none
              sm:rounded-br-none sm:rounded-md sm:translate-y-full transform
              transition duration-300 ease-in-out">
              <svg
                class="w-6 h-6 fill-current sm:text-white sm:w-8 sm:h-8"
                viewBox="0 0 20 20">
                <path
                  d="M9.999,8.472c-1.314,0-2.385,1.069-2.385,2.384c0,1.317,1.07,2.385,2.385,2.385c1.316,0,2.386-1.068,2.386-2.385C12.385,9.541,11.314,8.472,9.999,8.472z
                  M9.999,12.238c-0.76,0-1.38-0.622-1.38-1.382c0-0.761,0.62-1.38,1.38-1.38c0.761,0,1.38,0.62,1.38,1.38C11.379,11.616,10.76,12.238,9.999,12.238z" />
                <path
                  d="M15.232,5.375H9.398C9.159,4.366,8.247,3.61,7.174,3.61c-1.073,0-1.985,0.756-2.224,1.765H4.769c-1.246,0-2.259,1.012-2.259,2.257v6.499c0,1.247,1.014,2.259,2.259,2.259h10.464c1.244,0,2.258-1.012,2.258-2.259V7.632C17.49,6.387,16.477,5.375,15.232,5.375z
                  M16.486,14.131c0,0.69-0.564,1.256-1.254,1.256H4.769c-0.692,0-1.256-0.565-1.256-1.256V7.632c0-0.691,0.563-1.254,1.256-1.254H5.39c0.275,0,0.499-0.221,0.502-0.495c0.01-0.7,0.585-1.269,1.282-1.269s1.272,0.569,1.282,1.269c0.003,0.274,0.228,0.495,0.502,0.495h6.275c0.689,0,1.254,0.563,1.254,1.254V14.131z" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      <h1 class="text-2xl mt-12 text-gray-700">Gallery</h1>

      <!-- Error Handling -->
      <ErrorNotifier
        errors={updatesData.errors}
        errorKey="galleryUpdate"
        on:clearErrors={UpdatesStore.clearErrors.bind(this, 'galleryUpdate')} />

      {#if photoData.photos.length > 0}
        <div class="mt-4 flex flex-col sm:flex-row">
          <div
            class="w-full h-80 bg-grey-300 shadow-2xl relative rounded-md
            overflow-hidden border-2 hover:border-indigo-400 sm:w-10/12">
            <img
              src={photoData.photos[selectedGalleryImage].image}
              alt="model gallery"
              class="w-full h-full object-cover hover:scale-125 transform
              transition-all duration-500 ease-out" />

            <ChangeGalleryPicture
              pictureId={photoData.photos[selectedGalleryImage].id}
              size="w-8 h-8" />
          </div>
          <div
            class="pt-3 h-40 whitespace-no-wrap sm:w-3/12 sm:h-80 sm:ml-4
            sm:block sm:pt-0 sm:pr-2"
            data-simplebar>
            <!-- necessary div for the scrolling wheel to work -->
            <div>
              {#each photoData.photos as photo, i}
                <div
                  class="inline-block w-68 h-32 mr-2 bg-gray-200 cursor-pointer
                  rounded-md overflow-hidden border-2 hover:border-indigo-400
                  relative hover:opacity-100 sm:block sm:w-auto sm:mb-2 {selectedGalleryImage == i ? 'opacity-100' : 'opacity-50'}"
                  on:click={() => setSelectedGalleryImage(i)}>
                  <img
                    src={photo.image}
                    class="w-full h-full object-cover hover:scale-125 transform
                    transition-all duration-500 ease-out"
                    alt="model gallery {i}" />
                  <ChangeGalleryPicture pictureId={photoData.photos[i].id} />
                </div>
              {/each}
            </div>
          </div>
        </div>
      {:else}
        <p>No photos has been approved yet.</p>
      {/if}

      {#if photoData.photos.length < 8}
        <p class="mt-6 text-sm text-gray-600">
          You need to upload 8 photos for gallery. You have {photoData.photos.length}
          approved and {updatesData.gallery.length} update(s).
        </p>
        <div class="mt-4">
          <SaveButton text="START UPLOADING" on:click={onShowGalleryModal} />
        </div>
      {/if}

      <!-- on:dragenter|preventDefault|stopPropagation
    on:dragover|preventDefault|stopPropagation
    on:drop|preventDefault|stopPropagation={uploadPhotos} -->
    </div>
  {:else if tabName === tabs[1].name}
    <ProfilePicturesTab />
  {:else if tabName === tabs[2].name}
    <CoverPicturesTab />
  {:else if tabName === tabs[3].name}
    {#each updatesData.gallery as photo, index}
      <PhotoUpdateCard
        {photo}
        {index}
        fetching={uiData.fetching}
        on:update={({ detail: { file, photoId } }) => UpdatesStore.modifyGalleryPhotoUpdate(file, photoId)}
        on:delete={({ detail }) => UpdatesStore.deleteGalleryPhotoUpdate(detail)}
        on:clearErrors={UpdatesStore.clearGalleryPhotoErrors.bind(this, index)} />
    {:else}
      <p class="mt-4 text-gray-600">No Updates.</p>
    {/each}
  {/if}
</TabView>
