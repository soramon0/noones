<script>
  import Breadcrumb from "./shared/Breadcrumb";
  import FormInput from "./shared/FormInput";
  import UpdateButton from "./shared/UpdateButton";
  import Card from "./shared/Card"

  export let email;
  let submitted = false;
  const userData = {
    password: '',
    new_password: '',
    confirm_password: '',
    email,
  }

  const onValueChanged = ({ detail }) => {
    userData[detail.name] = detail.value;
  };

  const emailUpdate = async () => {
    submitted = true;    
    console.log(userData);
    submitted = false
  };

  const passwordUpdate = async () => {
    submitted = true;    
    console.log(userData);
    submitted = false
  };
  
</script>

<Breadcrumb activeText="User Settings" />

<div class="py-4 border-b-2 border-gray-200">
  <h2 class="text-lg">Email/Password</h2>
</div>
<div class="mt-4 flex flex-wrap justify-center">
  <Card classes="mb-4 h-40 sm:w-5/12 sm:mr-4">
    <form on:submit|preventDefault={emailUpdate}>
      <FormInput
        value={userData.email}
        type="email"
        name="email"
        label="E-mail Address"
        on:valueChanged={onValueChanged} />

      <UpdateButton />
    </form>
  </Card>
  
  <Card classes="sm:w-5/12">
    <form on:submit|preventDefault={passwordUpdate}>
      <FormInput
        value={userData.password}
        type="password"
        name="password"
        label="Current Password"
        on:valueChanged={onValueChanged} />
      <FormInput
        value={userData.new_password}
        type="password"
        name="new_password"
        label="New Password"
        on:valueChanged={onValueChanged} />
      <FormInput
        value={userData.confirm_password}
        type="password"
        name="confirm_password"
        label="Confirm New Password"
        on:valueChanged={onValueChanged} />
      <UpdateButton text="Update password" />
    </form>
  </Card>
</div>
