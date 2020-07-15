<script>
  import { onMount, onDestroy } from "svelte";
  import { fade, scale } from "svelte/transition";
  import PhotoStore from "../../store/photo";
  import UIStore from "../../store/ui";
  import UpdatesStore from "../../store/updates";
  import ErrorNotifier from "../shared/ErrorNotifier";
  import PopupErrorNotifier from "../shared/PopupErrorNotifier";
  import PhotoUpdateCard from "./PhotoUpdateCard";
  import PhotoCard from "./PhotoCard";
  import ToggleButton from "../shared/ToggleButton";

  $: photoData = $PhotoStore;
  $: uiData = $UIStore;
  $: updatesData = $UpdatesStore;

  let showUpdates = false;
  let io, target;

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
    target = document.querySelector(".fetch");
    io = new IntersectionObserver(handleIntersection, options);
    io.observe(target);
  });

  onDestroy(() => {
    io.unobserve(target);
  });

  $: console.log(photoData);
</script>

<div class="mt-4 mb-2 py-4 flex justify-between">
  {#if !showUpdates}
    <h2 class="text-xl text-gray-700 font-semibold tracking-wide">
      Profile Pictures
    </h2>
  {:else}
    <h2 class="text-xl text-gray-700 font-semibold tracking-wide">
      Profile Updates
    </h2>
  {/if}

  <ToggleButton bind:toggle={showUpdates} />
</div>

<PopupErrorNotifier
  errors={photoData.errors}
  errorKey="profilePicture"
  on:clearErrors={PhotoStore.clearErrors} />

{#if !showUpdates}
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
