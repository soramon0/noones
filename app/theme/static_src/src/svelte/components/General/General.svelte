<script>
  import { onMount } from "svelte";
  import { fade, fly } from "svelte/transition";
  import UserStore from "../../store/user";
  import UIStore from "../../store/ui";
  import UpdatesStore from "../../store/updates";
  import CancelButton from "../shared/CancelButton";
  import Card from "../shared/Card";
  import FormInput from "../shared/FormInput";
  import SuccessNotifier from "../shared/SuccessNotifier";
  import ErrorNotifier from "../shared/ErrorNotifier";
  import UpdateButton from "../shared/UpdateButton";
  import TabView from "../shared/TabView";

  export let model;
  export let errors;
  let tabs = [{ name: "Base" }, { name: "Updates" }];
  let tabName = tabs[0].name;

  $: UIData = $UIStore;
  $: updatesData = $UpdatesStore;
  $: isUpdateEmpty = Object.keys(updatesData.model).length;

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
    model[detail.name] = detail.value;
  };

  const onUpdateValueChanged = ({ detail }) => {
    updatesData.model[detail.name] = detail.value;
  };

  const onlyAdd = (...fields) => {
    const payload = { id: model.id };

    fields.forEach(field => {
      if (model[field]) payload[field] = model[field];
    });

    return payload;
  };

  const handleSubmit = async payloadType => {
    let payload = {};

    switch (payloadType.toLowerCase()) {
      case "profile":
        payload = onlyAdd(
          "first_name",
          "last_name",
          "phone",
          "birth_date",
          "sexe",
          "cin"
        );
        break;
      case "location":
        payload = onlyAdd("country", "city", "addresse", "zipcode");
        break;
      case "online":
        payload = onlyAdd("facebook", "instagram");
        break;
      default:
        payload = model;
    }

    await UserStore.updateModel(payload);

    // Show a success message
    window.scrollTo(0, 0);
    if (UIData.success) {
      // Hide the success message after 2 seconds
      setTimeout(() => {
        uiStore.setFeedbackModal(false);
      }, 2000);
    }
  };

  const createBioUpdate = async () => {
    await UpdatesStore.createModelUpdate({ bio: model.bio });

    scrollUpToSuccessMessage();
  };

  const modifyUpdateRequest = async () => {
    await UpdatesStore.modifyModelUpdate(model.id, {
      ...updatesData.model,
      model: model.id
    });

    scrollUpToSuccessMessage();
  };

  const removeUpdateRequest = async () => {
    await UpdatesStore.deleteModelUpdate(model.id);

    scrollUpToSuccessMessage();
  };

  onMount(() => {
    // Get user updates
    if (!isUpdateEmpty) {
      UpdatesStore.getModelUpdate();
    }
  });

  $: console.log(updatesData, isUpdateEmpty);
</script>

<TabView {tabs} {tabName} on:change={({ detail }) => (tabName = detail)} />

<SuccessNotifier />

{#if tabName === tabs[0].name}
  <div in:fly={{ x: -200, duration: 400 }} out:fade={{ duration: 100 }}>
    <Card title="Edit Profile">
      <form on:submit|preventDefault={handleSubmit.bind(this, 'profile')}>
        <div class="sm:flex sm:justify-center">
          <div class="w-full">
            <FormInput
              value={model.first_name}
              name="first_name"
              label="Nom"
              errors={errors['first_name']}
              on:valueChanged={onValueChanged} />
            <FormInput
              value={model.last_name}
              name="last_name"
              label="Prenom"
              errors={errors['last_name']}
              on:valueChanged={onValueChanged} />
            <FormInput
              value={model.phone}
              name="phone"
              label="Phone"
              errors={errors['phone']}
              on:valueChanged={onValueChanged} />
          </div>
          <div class="w-full mt-4 sm:mt-0 sm:ml-4">
            <FormInput
              value={model.birth_date}
              name="birth_date"
              label="Date de Niassance"
              errors={errors['birth_date']}
              on:valueChanged={onValueChanged} />
            <FormInput
              value={model.sexe}
              type="select"
              selectOptions={['f', 'h']}
              name="sexe"
              label="Sexe"
              errors={errors['sexe']}
              on:valueChanged={onValueChanged} />
            <FormInput
              value={model.cin}
              name="cin"
              label="CIN"
              errors={errors['cin']}
              on:valueChanged={onValueChanged} />
          </div>
        </div>
        <div class="text-right mt-2 sm:mt-4">
          <UpdateButton fetching={UIData.fetching} />
        </div>
      </form>
    </Card>

    <ErrorNotifier
      errors={updatesData.modelErrors}
      errorKey="model"
      on:clearErrors={UpdatesStore.clearModelErrors} />
    <Card
      title="About Me"
      description="This section must be filled in order to make your profile
      public.">
      <form on:submit|preventDefault={createBioUpdate}>
        <FormInput
          value={model.bio}
          type="textarea"
          name="bio"
          label="Bio"
          errors={updatesData.modelErrors['bio']}
          on:valueChanged={onValueChanged} />
        <div class="text-right mt-2 sm:mt-4">
          <UpdateButton fetching={UIData.fetching} />
        </div>
      </form>
    </Card>

    <Card title="Location">
      <form on:submit|preventDefault={handleSubmit.bind(this, 'location')}>
        <div class="sm:flex sm:justify-center">
          <div class="w-full">
            <FormInput
              value={model.country}
              name="country"
              label="Pays"
              errors={errors['country']}
              on:valueChanged={onValueChanged} />
            <FormInput
              value={model.addresse}
              name="addresse"
              label="Adresse"
              errors={errors['addresse']}
              on:valueChanged={onValueChanged} />
          </div>
          <div class="w-full mt-4 sm:mt-0 sm:ml-4">
            <FormInput
              value={model.city}
              name="city"
              label="Ville"
              errors={errors['city']}
              on:valueChanged={onValueChanged} />
            <FormInput
              value={model.zipcode}
              type="number"
              name="zipcode"
              label="Code Postal"
              errors={errors['zipcode']}
              on:valueChanged={onValueChanged} />
          </div>
        </div>
        <div class="text-right mt-2 sm:mt-4">
          <UpdateButton fetching={UIData.fetching} />
        </div>
      </form>
    </Card>

    <Card title="Online Presence">
      <form on:submit|preventDefault={handleSubmit.bind(this, 'online')}>
        <div class="sm:flex sm:justify-center">
          <div class="w-full">
            <FormInput
              value={model.facebook}
              name="facebook"
              label="Facebook"
              errors={errors['facebook']}
              on:valueChanged={onValueChanged} />
          </div>
          <div class="w-full mt-4 sm:mt-0 sm:ml-4">
            <FormInput
              value={model.instagram}
              name="instagram"
              label="Instagram"
              errors={errors['instagram']}
              on:valueChanged={onValueChanged} />
          </div>
        </div>
        <div class="text-right mt-2 sm:mt-4">
          <UpdateButton fetching={UIData.fetching} />
        </div>
      </form>
    </Card>
  </div>
{:else if tabName === tabs[1].name}
  <div in:fly={{ x: -200, duration: 400 }} out:fade={{ duration: 100 }}>
    {#if isUpdateEmpty}
      <ErrorNotifier
        errors={updatesData.model.errors}
        errorKey="model"
        on:clearErrors={UpdatesStore.clearModelUpdateErrors} />
      {#if updatesData.model.message.length}
        <Card
          classes={updatesData.model.accept ? 'border-green-300' : 'border-red-300'}>
          <h1 class="text-lg font-semibold">Response</h1>
          <p class="mt-2 text-sm text-gray-800">{updatesData.model.message}</p>
        </Card>
      {/if}
      <Card classes="mb-4">
        <form on:submit|preventDefault={modifyUpdateRequest}>
          <FormInput
            value={updatesData.model.bio}
            type="textarea"
            name="bio"
            label="Bio"
            errors={updatesData.model.errors['bio']}
            on:valueChanged={onUpdateValueChanged} />

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
