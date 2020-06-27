<script>
  import { onMount } from "svelte";
  import { fade, scale } from "svelte/transition";
  import PhotoStore from "../../store/photo";
  import UIStore from "../../store/ui";
  import UpdatesStore from "../../store/updates";
  import ErrorNotifier from "./ErrorNotifier";
  import PhotoUpdateCard from "./PhotoUpdateCard";
  import PhotoCard from "./PhotoCard";
  import ToggleButton from "./ToggleButton";

  $: photoData = $PhotoStore;
  $: uiData = $UIStore;
  $: updatesData = $UpdatesStore;

  let showProfileUpdates = false;

  async function handleIntersection(enteries) {
    if (enteries[0].isIntersecting) {
      if (photoData.profile.next) {
        await PhotoStore.getProfilePictures(photoData.profile.next);
      }
    }
  }

  onMount(async () => {
    const options = {
      root: null,
      rootMargins: "200px 0px 0px 0px",
      threshold: 0.5
    };

    if (!photoData.profile.data.length) {
      await PhotoStore.getProfilePictures();
    }

    const io = new IntersectionObserver(handleIntersection, options);
    io.observe(document.querySelector(".fetch"));
  });

  $: console.log(photoData);
</script>

<div class="mt-4 mb-2 flex justify-end">
  <ToggleButton bind:toggle={showProfileUpdates} />
</div>
{#if photoData.errors['profilePicture']}
  <div
    transition:scale
    class="p-4 w-11/12 fixed z-40 bg-white border-l-2 border-red-500 rounded-lg
    shadow-md sm:w-1/2">
    {#each photoData.errors['profilePicture'] as err}
      <p class="text-gray-600">{err}</p>
    {/each}
    <div class="mt-2 text-right">
      <button on:click={PhotoStore.clearErrors}>Close</button>
      <!-- <CancelButton on:click={toggleConfirm} />
          <SaveButton text="Remove" on:click={() => onRemove(photo.id)} /> -->
    </div>
  </div>
{/if}

{#if !showProfileUpdates}
  <div transition:fade class="mt-2 flex flex-wrap">

    {#each photoData.profile.data as photo, i}
      <PhotoCard
        {photo}
        on:mark={({ detail }) => PhotoStore.markProfilePicture(detail, i)}
        on:delete={({ detail }) => PhotoStore.deleteProfilePicture(detail)} />
    {:else}
      <p transition:fade class="mt-4 text-gray-600">No profile pictures.</p>
    {/each}
  </div>
  <div class="fetch h-10" />
{:else}
  {#each updatesData.profilePictures as photo, index}
    <PhotoUpdateCard
      {photo}
      {index}
      fetching={uiData.fetching}
      on:update={({ detail: { file, photoId } }) => UpdatesStore.modifyProfilePictureUpdate(file, photoId)}
      on:delete={({ detail }) => UpdatesStore.deleteProfilePictureUpdate(detail)}
      on:clearErrors={UpdatesStore.clearProfilePictureErrors.bind(this, index)} />
  {:else}
    <p class="mt-4 text-gray-600">No Updates.</p>
  {/each}
{/if}
