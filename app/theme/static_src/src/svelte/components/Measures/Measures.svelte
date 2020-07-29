<script>
  import { onMount } from "svelte";
  import { fade, fly } from "svelte/transition";
  import UIStore from "../../store/ui";
  import UpdatesStore from "../../store/updates";
  import Card from "../shared/Card";
  import FormInput from "../shared/FormInput";
  import UpdateButton from "../shared/UpdateButton";
  import CancelButton from "../shared/CancelButton";
  import SuccessNotifier from "../shared/SuccessNotifier";
  import ErrorNotifier from "../shared/ErrorNotifier";
  import TabView from "../shared/TabView";

  export let measures;
  let tabs = [{ name: "Base" }, { name: "Updates" }];
  let tabName = tabs[0].name;

  $: UIData = $UIStore;
  $: updatesData = $UpdatesStore;
  $: isUpdateEmpty = Object.keys(updatesData.measures).length;

  const scrollUpToSuccessMessage = () => {
    // Show a success message
    window.scrollTo(0, 0);
    if (UIData.success) {
      // Hide the success message after 2 seconds
      setTimeout(() => {
        UIStore.setFeedbackModal(false);
      }, 2000);
    }
  };

  const onValueChanged = ({ detail }) => {
    measures[detail.name] = detail.value;
  };

  const onUpdateValueChanged = ({ detail }) => {
    updatesData.measures[detail.name] = detail.value;
  };

  const createUpdateRequest = async () => {
    await UpdatesStore.createMeasuresUpdate({
      ...measures,
      measure: measures.id
    });

    scrollUpToSuccessMessage();
  };

  const modifyUpdateRequest = async () => {
    await UpdatesStore.modifyMeasuresUpdate(measures.id, {
      ...updatesData.measures,
      measure: measures.id
    });

    scrollUpToSuccessMessage();
  };

  const removeUpdateRequest = async () => {
    await UpdatesStore.deleteMeasuresUpdate(measures.id);

    scrollUpToSuccessMessage();
  };

  onMount(async () => {
    // Get user updates
    if (!isUpdateEmpty) {
      UpdatesStore.getMeasuresUpdate();
    }
  });
</script>

<TabView {tabs} {tabName} on:change={({ detail }) => (tabName = detail)} />

<SuccessNotifier />

{#if tabName === tabs[0].name}
  <div in:fly={{ x: -200, duration: 400 }} out:fade={{ duration: 100 }}>
    <ErrorNotifier
      errors={updatesData.measuresErrors}
      errorKey="measure"
      on:clearErrors={UpdatesStore.clearMeasuresErrors} />
    <Card classes="mb-4">
      <form on:submit|preventDefault={createUpdateRequest}>
        <div class="sm:flex sm:justify-center">
          <div class="w-full">
            <FormInput
              value={measures.buste}
              type="number"
              name="buste"
              label="Buste"
              errors={updatesData.measuresErrors['buste']}
              on:valueChanged={onValueChanged} />
            <FormInput
              value={measures.taillenombrill}
              type="number"
              name="taillenombrill"
              label="Taille nombrill"
              errors={updatesData.measuresErrors['taillenombrill']}
              on:valueChanged={onValueChanged} />
            <FormInput
              value={measures.taille}
              type="number"
              name="taille"
              label="Taille"
              errors={updatesData.measuresErrors['taille']}
              on:valueChanged={onValueChanged} />
            <FormInput
              value={measures.pointure}
              type="number"
              name="pointure"
              label="Pointure"
              errors={updatesData.measuresErrors['pointure']}
              on:valueChanged={onValueChanged} />
            <FormInput
              value={measures.epaules}
              type="number"
              name="epaules"
              label="Epaules"
              errors={updatesData.measuresErrors['epaules']}
              on:valueChanged={onValueChanged} />
          </div>
          <div class="w-full mt-4 sm:mt-0 sm:ml-4">
            <FormInput
              value={measures.hanches}
              type="number"
              name="hanches"
              label="Hanches"
              errors={updatesData.measuresErrors['hanches']}
              on:valueChanged={onValueChanged} />
            <FormInput
              value={measures.poids}
              type="number"
              name="poids"
              label="Poids"
              errors={updatesData.measuresErrors['poids']}
              on:valueChanged={onValueChanged} />
            <FormInput
              value={measures.yeux}
              name="yeux"
              label="Yeux"
              errors={updatesData.measuresErrors['yeux']}
              on:valueChanged={onValueChanged} />
            <FormInput
              value={measures.cheveux}
              name="cheveux"
              label="Cheveux"
              errors={updatesData.measuresErrors['cheveux']}
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
        errorKey="measure"
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
                value={updatesData.measures.buste}
                type="number"
                name="buste"
                label="Buste"
                errors={updatesData.measures.errors['buste']}
                on:valueChanged={onUpdateValueChanged} />
              <FormInput
                value={updatesData.measures.taillenombrill}
                type="number"
                name="taillenombrill"
                label="Taille nombrill"
                errors={updatesData.measures.errors['taillenombrill']}
                on:valueChanged={onUpdateValueChanged} />
              <FormInput
                value={updatesData.measures.taille}
                type="number"
                name="taille"
                label="Taille"
                errors={updatesData.measures.errors['taille']}
                on:valueChanged={onUpdateValueChanged} />
              <FormInput
                value={updatesData.measures.pointure}
                type="number"
                name="pointure"
                label="Pointure"
                errors={updatesData.measures.errors['pointure']}
                on:valueChanged={onUpdateValueChanged} />
              <FormInput
                value={updatesData.measures.epaules}
                type="number"
                name="epaules"
                label="Epaules"
                errors={updatesData.measures.errors['epaules']}
                on:valueChanged={onUpdateValueChanged} />
            </div>
            <div class="w-full mt-4 sm:mt-0 sm:ml-4">
              <FormInput
                value={updatesData.measures.hanches}
                type="number"
                name="hanches"
                label="Hanches"
                errors={updatesData.measures.errors['hanches']}
                on:valueChanged={onUpdateValueChanged} />
              <FormInput
                value={updatesData.measures.poids}
                type="number"
                name="poids"
                label="Poids"
                errors={updatesData.measures.errors['poids']}
                on:valueChanged={onUpdateValueChanged} />
              <FormInput
                value={updatesData.measures.yeux}
                name="yeux"
                label="Yeux"
                errors={updatesData.measures.errors['yeux']}
                on:valueChanged={onUpdateValueChanged} />
              <FormInput
                value={updatesData.measures.cheveux}
                name="cheveux"
                label="Cheveux"
                errors={updatesData.measures.errors['cheveux']}
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