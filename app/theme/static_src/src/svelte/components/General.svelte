<script>
  import userStore from '../store/main'
  import Breadcrumb from "./shared/Breadcrumb";
  import Card from './shared/Card'
  import FormInput from "./shared/FormInput";

  export let model;
  export let errors;
  let submitted = false;

  const onValueChanged = ({ detail }) => {
    model[detail.name] = detail.value;
  };

  const handleSubmit = async () => {
    submitted = true;
    await userStore.updateModel(model)
    submitted = false
  };
</script>

<Breadcrumb activeText="General" />

<Card>
  <form on:submit|preventDefault={handleSubmit}>
    <div class="sm:flex sm:justify-center">
      <div class="sm:w-64 md:w-5/12">
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
        <FormInput
          value={model.country}
          name="country"
          label="Pays"
          errors={errors['country']}
          on:valueChanged={onValueChanged} />
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
        <FormInput
          value={model.addresse}
          name="addresse"
          label="Adresse"
          errors={errors['addresse']}
          on:valueChanged={onValueChanged} />
      </div>
      <div class="mt-4 sm:mt-0 sm:ml-4 sm:w-64 md:w-5/12">
        <FormInput
          value={model.facebook}
          name="facebook"
          label="Facebook"
          errors={errors['facebook']}
          on:valueChanged={onValueChanged} />
        <FormInput
          value={model.instagram}
          name="instagram"
          label="Instagram"
          errors={errors['instagram']}
          on:valueChanged={onValueChanged} />
        <FormInput
          value={model.birth_date}
          name="birth_date"
          label="Date de Niassance"
          errors={errors['birth_date']}
          on:valueChanged={onValueChanged} />
        <FormInput
          value={model.sexe}
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
        <FormInput
          value={model.bio}
          name="bio"
          label="Bio"
          errors={errors['bio']}
          on:valueChanged={onValueChanged} />
      </div>
    </div>
    <div class="text-right mt-6">
      <button
        class="btn-black capitalize hover:bg-gray-700 sm:w-auto {submitted ? 'bg-gray-700 cursor-not-allowed' : ''}"
        disabled={submitted}>
        Update
      </button>
    </div>
  </form>
</Card>
