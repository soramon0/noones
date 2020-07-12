<script>
  import { onMount, onDestroy } from "svelte";
  import { fade, scale } from "svelte/transition";
  import PhotoStore from "../../store/photo";
  import UIStore from "../../store/ui";
  import UpdatesStore from "../../store/updates";
  import ErrorNotifier from "../shared/ErrorNotifier";
  import ToggleButton from "../shared/ToggleButton";
  import PopupErrorNotifier from "../shared/PopupErrorNotifier";
  import PhotoUpdateCard from "./PhotoUpdateCard";
  import PhotoCard from "./PhotoCard";

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

<div class="mt-4 mb-2 flex justify-end">
  <ToggleButton bind:toggle={showUpdates} />
</div>

<PopupErrorNotifier
  errors={photoData.errors}
  errorKey="coverPicture"
  on:clearErrors={PhotoStore.clearErrors} />

{#if !showUpdates}
  <div transition:fade class="mt-2 flex flex-wrap">
    {#each photoData.cover.data as photo, i}
      <PhotoCard
        markText="Mark as Cover Picture"
        {photo}
        on:mark={({ detail }) => PhotoStore.markCoverPicture(detail, i)}
        on:delete={({ detail }) => PhotoStore.deleteCoverPicture(detail)} />
    {:else}
      <p transition:fade class="mt-4 text-gray-600">No cover pictures.</p>
    {/each}
  </div>
  <div class="fetch h-10" />
{:else}
  {#each updatesData.coverPictures as photo, index}
    <PhotoUpdateCard
      {photo}
      {index}
      fetching={uiData.fetching}
      on:update={({ detail: { file, photoId } }) => UpdatesStore.modifyCoverPictureUpdate(file, photoId)}
      on:delete={({ detail }) => UpdatesStore.deleteCoverPictureUpdate(detail)}
      on:clearErrors={UpdatesStore.clearCoverPictureErrors.bind(this, index)} />
  {:else}
    <p class="mt-4 text-gray-600">No Updates.</p>
  {/each}
{/if}
