<script>
  import userStore from "../store/main";
  import uiStore from "../store/ui";
  import Breadcrumb from "./shared/Breadcrumb";
  import Card from "./shared/Card";
  import FormInput from "./shared/FormInput";
  import UpdateButton from "./shared/UpdateButton";
  import SuccessNotifier from "./shared/SuccessNotifier";

  export let measures;
  export let errors;
  $: uiData = $uiStore;

  const onValueChanged = ({ detail }) => {
    measures[detail.name] = detail.value;
  };

  const handleSubmit = async () => {
    await userStore.updateMeasures(measures);

    // Show a success message
    window.scrollTo(0, 0);
    if (uiData.success) {
      // Hide the success message after 2 seconds
      setTimeout(() => {
        uiStore.setSuccess(false);
      }, 2000);
    }
  };
</script>

<Breadcrumb activeText="Measures" />

<SuccessNotifier response={uiData.success} />

<Card classes="mb-48">
  <form on:submit|preventDefault={handleSubmit}>
    <div class="sm:flex sm:justify-center">
      <div class="sm:w-64 md:w-5/12">
        <FormInput
          value={measures.buste}
          type="number"
          name="buste"
          label="Buste"
          errors={errors['buste']}
          on:valueChanged={onValueChanged} />
        <FormInput
          value={measures.taillenombrill}
          type="number"
          name="taillenombrill"
          label="Taille nombrill"
          errors={errors['taillenombrill']}
          on:valueChanged={onValueChanged} />
        <FormInput
          value={measures.taille}
          type="number"
          name="taille"
          label="Taille"
          errors={errors['taille']}
          on:valueChanged={onValueChanged} />
        <FormInput
          value={measures.pointure}
          type="number"
          name="pointure"
          label="Pointure"
          errors={errors['pointure']}
          on:valueChanged={onValueChanged} />
        <FormInput
          value={measures.epaules}
          type="number"
          name="epaules"
          label="Epaules"
          errors={errors['epaules']}
          on:valueChanged={onValueChanged} />
      </div>
      <div class="mt-4 sm:mt-0 sm:ml-4 sm:w-64 md:w-5/12">
        <FormInput
          value={measures.hanches}
          type="number"
          name="hanches"
          label="Hanches"
          errors={errors['hanches']}
          on:valueChanged={onValueChanged} />
        <FormInput
          value={measures.poids}
          type="number"
          name="poids"
          label="Poids"
          errors={errors['poids']}
          on:valueChanged={onValueChanged} />
        <FormInput
          value={measures.yeux}
          name="yeux"
          label="Yeux"
          errors={errors['yeux']}
          on:valueChanged={onValueChanged} />
        <FormInput
          value={measures.cheveux}
          name="cheveux"
          label="Cheveux"
          errors={errors['cheveux']}
          on:valueChanged={onValueChanged} />
      </div>
    </div>
    <UpdateButton fetching={uiData.fetching} />
  </form>
</Card>
