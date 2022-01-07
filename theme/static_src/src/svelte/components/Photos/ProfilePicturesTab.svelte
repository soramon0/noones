<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { fade, scale } from 'svelte/transition';
  import { UIStore, PhotoStore, UpdatesStore } from '../../store/index';
  import ErrorNotifier from '../shared/ErrorNotifier.svelte';
  import PopupErrorNotifier from '../shared/PopupErrorNotifier.svelte';
  import PhotoUpdateCard from './PhotoUpdateCard.svelte';
  import PhotoCard from './PhotoCard.svelte';
  import ToggleButton from '../shared/ToggleButton.svelte';

  $: photoData = $PhotoStore;
  $: UIData = $UIStore;
  $: updatesData = $UpdatesStore;

  let showUpdates = false;
  let io: IntersectionObserver, target: Element;

  async function handleIntersection(enteries: IntersectionObserverEntry[]) {
    if (enteries[0].isIntersecting) {
      if (photoData.profile.next) {
        await PhotoStore.getProfilePictures(photoData.profile.next);
      }
    }
  }

  onMount(async () => {
    if (!photoData.profile.data.length) {
      await PhotoStore.getProfilePictures();
    }

    const options = {
      root: null,
      rootMargin: '200px 0px 0px 0px',
      threshold: 0.5,
    };
    target = document.querySelector('.fetch');
    io = new IntersectionObserver(handleIntersection, options);
    io.observe(target);
  });

  onDestroy(() => {
    io.unobserve(target);
  });
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
        fetching={UIData.fetching}
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
      fetching={UIData.fetching}
      on:update={({ detail: { file, photoId } }) => UpdatesStore.modifyProfilePictureUpdate(file, photoId)}
      on:delete={({ detail }) => UpdatesStore.deleteProfilePictureUpdate(detail)}
      on:clearErrors={UpdatesStore.clearProfilePictureErrors.bind(this, index)} />
  {:else}
    <p class="mt-4 text-gray-600">No Updates.</p>
  {/each}
{/if}
