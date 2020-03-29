<script>
  import Breadcrumb from "./shared/Breadcrumb";
  import TextInput from "./shared/TextInput";
  export let model;

  let submitted = false;

  const onValueChanged = ({ detail }) => {
    model[detail.name] = detail.value;
  };

  const handleSubmit = () => {
    submitted = true;
    console.log(model);
  };
</script>

<Breadcrumb activeText="General" />

<form
  on:submit|preventDefault={handleSubmit}
  class="p-4 w-full bg-white shadow rounded-lg">
  <div class="sm:flex sm:justify-center">
    <div class="sm:w-64 md:w-5/12">
      <TextInput
        value={model.first_name}
        name="first_name"
        label="Nom"
        on:valueChanged={onValueChanged} />
      <TextInput
        value={model.last_name}
        name="last_name"
        label="Prenom"
        on:valueChanged={onValueChanged} />
      <TextInput
        value={model.phone}
        name="phone"
        label="Phone"
        on:valueChanged={onValueChanged} />
      <TextInput
        value={model.country}
        name="country"
        label="Pays"
        on:valueChanged={onValueChanged} />
      <TextInput
        value={model.city}
        name="city"
        label="Ville"
        on:valueChanged={onValueChanged} />
      <TextInput
        value={model.zipcode}
        type="number"
        name="zipcode"
        label="Code Postal"
        on:valueChanged={onValueChanged} />
      <TextInput
        value={model.addresse}
        name="addresse"
        label="Adresse"
        on:valueChanged={onValueChanged} />
    </div>
    <div class="mt-4 sm:mt-0 sm:ml-4 sm:w-64 md:w-5/12">
      <TextInput
        value={model.facebook}
        name="facebook"
        label="Facebook"
        on:valueChanged={onValueChanged} />
      <TextInput
        value={model.instagram}
        name="instagram"
        label="Instagram"
        on:valueChanged={onValueChanged} />
      <TextInput
        value={model.birth_date}
        name="birth_date"
        label="Date de Niassance"
        on:valueChanged={onValueChanged} />
      <TextInput
        value={model.sexe}
        name="sexe"
        label="Sexe"
        on:valueChanged={onValueChanged} />
      <TextInput
        value={model.cin}
        name="cin"
        label="CIN"
        on:valueChanged={onValueChanged} />
      <TextInput
        value={model.bio}
        name="bio"
        label="Bio"
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
