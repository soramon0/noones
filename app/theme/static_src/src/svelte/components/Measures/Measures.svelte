<script lang="ts">
  import { onMount } from 'svelte';
  import { fade, fly } from 'svelte/transition';
  import { UIStore, UpdatesStore } from '../../store/index';
  import type { IMeasures } from '../../types/models';
  import Card from '../shared/Card.svelte';
  import FormInput from '../shared/FormInput.svelte';
  import UpdateButton from '../shared/UpdateButton.svelte';
  import CancelButton from '../shared/CancelButton.svelte';
  import SuccessNotifier from '../shared/SuccessNotifier.svelte';
  import ErrorNotifier from '../shared/ErrorNotifier.svelte';
  import TabView from '../shared/TabView.svelte';

  export let measures: IMeasures;

  let tabs = [{ name: 'Base' }, { name: 'Updates' }];
  let tabName = tabs[0].name;

  $: UIData = $UIStore;
  $: updatesData = $UpdatesStore;
  $: isUpdateEmpty = Object.keys(updatesData.measures).length;

  const scrollUpToSuccessMessage = () => {
    // Show a success message
    window.scrollTo(0, 0);
    // TODO(karim): find what condition implies succes
    // if (UIData.success) {
    //   // Hide the success message after 2 seconds
    //   setTimeout(() => {
    //     UIStore.setFeedbackModal(false);
    //   }, 2000);
    // }
  };

  const onValueChanged = ({ detail }) => {
    measures[detail.name] = detail.value;
  };

  const onUpdateValueChanged = ({ detail }) => {
    updatesData.measures[detail.name] = detail.value;
  };

  const createUpdateRequest = async () => {
    await UpdatesStore.createMeasuresUpdate(measures);

    scrollUpToSuccessMessage();
  };

  const modifyUpdateRequest = async () => {
    const { measures: measuresUpdate } = updatesData;
    await UpdatesStore.modifyMeasuresUpdate(measuresUpdate.id, measuresUpdate);

    scrollUpToSuccessMessage();
  };

  const removeUpdateRequest = async () => {
    await UpdatesStore.deleteMeasuresUpdate(updatesData.measures.id);

    scrollUpToSuccessMessage();
  };

  onMount(async () => {
    // Get user updates
    if (!isUpdateEmpty) {
      UpdatesStore.getMeasuresUpdate();
    }
  });

  $: console.log(updatesData);
</script>

<TabView {tabs} {tabName} on:change={({ detail }) => (tabName = detail)} />

<SuccessNotifier />

{#if tabName === tabs[0].name}
  <div in:fly={{ x: -200, duration: 400 }} out:fade={{ duration: 100 }}>
    <ErrorNotifier
      errors={updatesData.errors}
      errorKey="measures"
      on:clearErrors={() => UpdatesStore.clearErrors('measures')} />
    <Card classes="mb-4">
      <form on:submit|preventDefault={createUpdateRequest}>
        <div class="sm:flex sm:justify-center">
          <div class="w-full">
            <FormInput
              value={measures.bust}
              type="number"
              name="bust"
              label="Buste"
              errors={updatesData.errors['bust']}
              on:valueChanged={onValueChanged} />
            <FormInput
              value={measures.waist}
              type="number"
              name="waist"
              label="Taille nombrill"
              errors={updatesData.errors['waist']}
              on:valueChanged={onValueChanged} />
            <FormInput
              value={measures.height}
              type="number"
              name="height"
              label="Taille"
              errors={updatesData.errors['height']}
              on:valueChanged={onValueChanged} />
            <FormInput
              value={measures.shoe_size}
              type="number"
              name="shoe_size"
              label="Pointure"
              errors={updatesData.errors['shoe_size']}
              on:valueChanged={onValueChanged} />
            <FormInput
              value={measures.shoulders}
              type="number"
              name="shoulders"
              label="Epaules"
              errors={updatesData.errors['shoulders']}
              on:valueChanged={onValueChanged} />
          </div>
          <div class="w-full mt-4 sm:mt-0 sm:ml-4">
            <FormInput
              value={measures.hips}
              type="number"
              name="hips"
              label="Hanches"
              errors={updatesData.errors['hips']}
              on:valueChanged={onValueChanged} />
            <FormInput
              value={measures.weight}
              type="number"
              name="weight"
              label="Poids"
              errors={updatesData.errors['weight']}
              on:valueChanged={onValueChanged} />
            <FormInput
              value={measures.eyes}
              name="eyes"
              label="Yeux"
              errors={updatesData.errors['eyes']}
              on:valueChanged={onValueChanged} />
            <FormInput
              value={measures.hair}
              name="hair"
              label="Cheveux"
              errors={updatesData.errors['hair']}
              on:valueChanged={onValueChanged} />
          </div>
        </div>
        <div class="text-right mt-2">
          <UpdateButton text="Create Update" fetching={UIData.fetching} />
        </div>
      </form>
    </Card>
  </div>
{:else if tabName === tabs[1].name}
  <div in:fly={{ x: -200, duration: 400 }} out:fade={{ duration: 100 }}>
    {#if isUpdateEmpty}
      <ErrorNotifier
        errors={updatesData.measures.errors}
        errorKey="measures"
        on:clearErrors={UpdatesStore.clearMeasuresUpdateErrors} />
      {#if updatesData.measures.message.length}
        <Card
          classes={updatesData.measures.accept ? 'border-green-300' : 'border-red-300'}>
          <h1 class="text-lg font-semibold">Response</h1>
          <p class="mt-2 text-sm text-gray-800">
            {updatesData.measures.message}
          </p>
        </Card>
      {/if}
      <Card classes="mb-4">
        <form on:submit|preventDefault={modifyUpdateRequest}>
          <div class="sm:flex sm:justify-center">
            <div class="w-full">
              <FormInput
                value={updatesData.measures.bust}
                type="number"
                name="bust"
                label="Buste"
                errors={updatesData.measures.errors['bust']}
                on:valueChanged={onUpdateValueChanged} />
              <FormInput
                value={updatesData.measures.waist}
                type="number"
                name="waist"
                label="Taille nombrill"
                errors={updatesData.measures.errors['waist']}
                on:valueChanged={onUpdateValueChanged} />
              <FormInput
                value={updatesData.measures.height}
                type="number"
                name="height"
                label="Taille"
                errors={updatesData.measures.errors['height']}
                on:valueChanged={onUpdateValueChanged} />
              <FormInput
                value={updatesData.measures.shoe_size}
                type="number"
                name="shoe_size"
                label="Pointure"
                errors={updatesData.measures.errors['shoe_size']}
                on:valueChanged={onUpdateValueChanged} />
              <FormInput
                value={updatesData.measures.shoulders}
                type="number"
                name="shoulders"
                label="Epaules"
                errors={updatesData.measures.errors['shoulders']}
                on:valueChanged={onUpdateValueChanged} />
            </div>
            <div class="w-full mt-4 sm:mt-0 sm:ml-4">
              <FormInput
                value={updatesData.measures.hips}
                type="number"
                name="hips"
                label="Hanches"
                errors={updatesData.measures.errors['hips']}
                on:valueChanged={onUpdateValueChanged} />
              <FormInput
                value={updatesData.measures.weight}
                type="number"
                name="weight"
                label="Poids"
                errors={updatesData.measures.errors['weight']}
                on:valueChanged={onUpdateValueChanged} />
              <FormInput
                value={updatesData.measures.eyes}
                name="eyes"
                label="Yeux"
                errors={updatesData.measures.errors['eyes']}
                on:valueChanged={onUpdateValueChanged} />
              <FormInput
                value={updatesData.measures.hair}
                name="hair"
                label="Cheveux"
                errors={updatesData.measures.errors['hair']}
                on:valueChanged={onUpdateValueChanged} />
            </div>
          </div>
          <div class="flex justify-end items-center mt-2 space-x-4">
            <CancelButton
              text="Remove"
              fetching={UIData.fetching}
              on:click={removeUpdateRequest} />
            <UpdateButton type="submit" fetching={UIData.fetching} />
          </div>
        </form>
      </Card>
    {:else}
      <p class="mt-6 text-gray-700">No Updates</p>
    {/if}
  </div>
{/if}
