<script>
  import UIStore from "../../store/ui";
  import UserStore from "../../store/user";
  import Breadcrumb from "../shared/Breadcrumb";
  import FormInput from "../shared/FormInput";
  import UpdateButton from "../shared/UpdateButton";
  import Card from "../shared/Card";
  import SuccessNotifier from "../shared/SuccessNotifier";

  export let email;
  $: uiData = $UIStore;
  $: userData = $UserStore;
  const passwordPayload = {
    password: "",
    new_password: "",
    confirm_password: ""
  };

  const onValueChanged = ({ detail }) => {
    userData[detail.name] = detail.value;
  };

  const emailUpdate = async () => {
    console.log(email);
  };

  const passwordUpdate = async () => {
    await UserStore.updatePassword(passwordPayload);

    if (Object.keys(userData.errors).length === 0) {
      passwordPayload.password = "";
      passwordPayload.new_password = "";
      passwordPayload.confirm_password = "";
    }
  };
</script>

<Breadcrumb activeText="User Settings" />
<SuccessNotifier />

<Card title="Change Your Email">
  <form on:submit|preventDefault={emailUpdate}>
    <FormInput
      bind:value={email}
      type="email"
      name="email"
      label="E-mail Address"
      on:valueChanged={({ detail }) => (email = detail.value)} />
    <div class="text-right mt-2">
      <UpdateButton text="Update Email" />
    </div>
  </form>
</Card>

<Card title="Change Your Password">
  <form on:submit|preventDefault={passwordUpdate}>
    <FormInput
      bind:value={passwordPayload.password}
      type="password"
      name="password"
      label="Current Password"
      errors={userData.errors['password']}
      on:valueChanged={onValueChanged} />
    <FormInput
      bind:value={passwordPayload.new_password}
      type="password"
      name="new_password"
      label="New Password"
      errors={userData.errors['new_password']}
      on:valueChanged={onValueChanged} />
    <FormInput
      bind:value={passwordPayload.confirm_password}
      type="password"
      name="confirm_password"
      label="Confirm New Password"
      errors={userData.errors['confirm_password']}
      on:valueChanged={onValueChanged} />
    <div class="text-right mt-2">
      <UpdateButton text="Update password" />
    </div>
  </form>
</Card>
