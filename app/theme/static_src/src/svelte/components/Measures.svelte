<script>
  import { onMount } from "svelte";
  import { fade, fly } from "svelte/transition";
  import userStore from "../store/main";
  import uiStore from "../store/ui";
  import UpdatesStore from "../store/updates";
  import Card from "./shared/Card";
  import FormInput from "./shared/FormInput";
  import UpdateButton from "./shared/UpdateButton";
  import CancelButton from "./shared/CancelButton";
  import SuccessNotifier from "./shared/SuccessNotifier";
  import ErrorNotifier from "./shared/ErrorNotifier";
  import TabView from "./shared/TabView";
  import Breadcrumb from "./shared/Breadcrumb";

  export let measures;

  $: uiData = $uiStore;
  $: updatesData = $UpdatesStore;

  let currentTab = 0;
  let tabs = [{ name: "Base", show: true }, { name: "Updates", show: false }];

  const onValueChanged = ({ detail }) => {
    measures[detail.name] = detail.value;
  };

  const onUpdateValueChanged = ({ detail }) => {
    updatesData.measures[detail.name] = detail.value;
  };

  const sendUpdateRequest = async () => {
    await UpdatesStore.createMeasuresUpdate({
      ...measures,
      measure: measures.id
    });

    // Only show the updates tab when we have updates
    if (Object.keys(updatesData.measures).length !== 0) {
      tabs = [tabs[0], { ...tabs[1], show: true }];
    }

    // Show a success message
    window.scrollTo(0, 0);
    if (uiData.success) {
      // Hide the success message after 2 seconds
      setTimeout(() => {
        uiStore.setFeedbackModal(false);
      }, 2000);
    }
  };

  const updateUpdateRequest = async () => {
    await UpdatesStore.updateMeasures(measures.id, {
      ...updatesData.measures,
      measure: measures.id
    });

    // Only show the updates tab when we have updates
    if (Object.keys(updatesData.measures).length === 0) {
      tabs = [tabs[0], { ...tabs[1], show: false }];
      currentTab = 0;
    }

    // Show a success message
    window.scrollTo(0, 0);
    if (uiData.success) {
      // Hide the success message after 2 seconds
      setTimeout(() => {
        uiStore.setFeedbackModal(false);
      }, 2000);
    }
  };

  const removeUpdateRequest = async () => {
    await UpdatesStore.deleteMeasuresUpdate(measures.id);

    // Only show the updates tab when we have updates
    if (Object.keys(updatesData.measures).length === 0) {
      tabs = [tabs[0], { ...tabs[1], show: false }];
      currentTab = 0;
    }

    // Show a success message
    window.scrollTo(0, 0);
    if (uiData.success) {
      // Hide the success message after 2 seconds
      setTimeout(() => {
        uiStore.setFeedbackModal(false);
      }, 2000);
    }
  };

  onMount(async () => {
    // Get user updates
    if (Object.keys(updatesData.measures).length === 0) {
      await UpdatesStore.getMeasures(measures.id);
    }

    // Only show the updates tab when we have updates
    if (Object.keys(updatesData.measures).length !== 0) {
      tabs = [tabs[0], { ...tabs[1], show: true }];
    }
  });

  $: console.log(updatesData);
</script>

<Breadcrumb activeText="Measurements" />

<TabView
  {tabs}
  {currentTab}
  on:change={({ detail }) => (currentTab = detail)} />

<SuccessNotifier />
<ErrorNotifier errors={updatesData.errors} errorKey="measure" />

{#if currentTab === 0}
  <div in:fly={{ x: -200, duration: 400 }} out:fade={{ duration: 100 }}>
    <Card classes="mb-4">
      <form on:submit|preventDefault={sendUpdateRequest}>
        <div class="sm:flex sm:justify-center">
          <div class="w-full">
            <FormInput
              value={measures.buste}
              type="number"
              name="buste"
              label="Buste"
              errors={updatesData.errors['buste']}
              on:valueChanged={onValueChanged} />
            <FormInput
              value={measures.taillenombrill}
              type="number"
              name="taillenombrill"
              label="Taille nombrill"
              errors={updatesData.errors['taillenombrill']}
              on:valueChanged={onValueChanged} />
            <FormInput
              value={measures.taille}
              type="number"
              name="taille"
              label="Taille"
              errors={updatesData.errors['taille']}
              on:valueChanged={onValueChanged} />
            <FormInput
              value={measures.pointure}
              type="number"
              name="pointure"
              label="Pointure"
              errors={updatesData.errors['pointure']}
              on:valueChanged={onValueChanged} />
            <FormInput
              value={measures.epaules}
              type="number"
              name="epaules"
              label="Epaules"
              errors={updatesData.errors['epaules']}
              on:valueChanged={onValueChanged} />
          </div>
          <div class="w-full mt-4 sm:mt-0 sm:ml-4">
            <FormInput
              value={measures.hanches}
              type="number"
              name="hanches"
              label="Hanches"
              errors={updatesData.errors['hanches']}
              on:valueChanged={onValueChanged} />
            <FormInput
              value={measures.poids}
              type="number"
              name="poids"
              label="Poids"
              errors={updatesData.errors['poids']}
              on:valueChanged={onValueChanged} />
            <FormInput
              value={measures.yeux}
              name="yeux"
              label="Yeux"
              errors={updatesData.errors['yeux']}
              on:valueChanged={onValueChanged} />
            <FormInput
              value={measures.cheveux}
              name="cheveux"
              label="Cheveux"
              errors={updatesData.errors['cheveux']}
              on:valueChanged={onValueChanged} />
          </div>
        </div>
        <div class="text-right mt-2">
          <UpdateButton text="Send Update Request" fetching={uiData.fetching} />
        </div>
      </form>
    </Card>
  </div>
{:else if currentTab === 1 && Object.keys(updatesData.measures).length}
  <div in:fly={{ x: -200, duration: 400 }} out:fade={{ duration: 100 }}>
    {#if updatesData.measures.message.length}
      <Card
        classes={updatesData.measures.accept ? 'border-green-300' : 'border-red-300'}>
        <h1 class="text-lg font-semibold">Response</h1>
        <p class="mt-2 text-sm text-gray-800">{updatesData.measures.message}</p>
      </Card>
    {/if}
    <Card classes="mb-4">
      <form on:submit|preventDefault={sendUpdateRequest}>
        <div class="sm:flex sm:justify-center">
          <div class="w-full">
            <FormInput
              value={updatesData.measures.buste}
              type="number"
              name="buste"
              label="Buste"
              errors={updatesData.errors['buste']}
              on:valueChanged={onUpdateValueChanged} />
            <FormInput
              value={updatesData.measures.taillenombrill}
              type="number"
              name="taillenombrill"
              label="Taille nombrill"
              errors={updatesData.errors['taillenombrill']}
              on:valueChanged={onUpdateValueChanged} />
            <FormInput
              value={updatesData.measures.taille}
              type="number"
              name="taille"
              label="Taille"
              errors={updatesData.errors['taille']}
              on:valueChanged={onUpdateValueChanged} />
            <FormInput
              value={updatesData.measures.pointure}
              type="number"
              name="pointure"
              label="Pointure"
              errors={updatesData.errors['pointure']}
              on:valueChanged={onUpdateValueChanged} />
            <FormInput
              value={updatesData.measures.epaules}
              type="number"
              name="epaules"
              label="Epaules"
              errors={updatesData.errors['epaules']}
              on:valueChanged={onUpdateValueChanged} />
          </div>
          <div class="w-full mt-4 sm:mt-0 sm:ml-4">
            <FormInput
              value={updatesData.measures.hanches}
              type="number"
              name="hanches"
              label="Hanches"
              errors={updatesData.errors['hanches']}
              on:valueChanged={onUpdateValueChanged} />
            <FormInput
              value={updatesData.measures.poids}
              type="number"
              name="poids"
              label="Poids"
              errors={updatesData.errors['poids']}
              on:valueChanged={onUpdateValueChanged} />
            <FormInput
              value={updatesData.measures.yeux || ''}
              name="yeux"
              label="Yeux"
              errors={updatesData.errors['yeux']}
              on:valueChanged={onUpdateValueChanged} />
            <FormInput
              value={updatesData.measures.cheveux || ''}
              name="cheveux"
              label="Cheveux"
              errors={updatesData.errors['cheveux']}
              on:valueChanged={onUpdateValueChanged} />
          </div>
        </div>
        <div class="flex justify-end items-center mt-2 space-x-4">
          <CancelButton
            text="Remove"
            fetching={uiData.fetching}
            on:click={removeUpdateRequest} />
          <UpdateButton
            type="button"
            fetching={uiData.fetching}
            on:click={updateUpdateRequest} />
        </div>
      </form>
    </Card>
  </div>
{/if}
