<script>
  import Breadcrumb from "./shared/Breadcrumb";
  export let modelStore;

</script>

<Breadcrumb activeText="User Settings" />

<div class="container px-4 mt-4 sm:mx-auto sm:p-0">
  <div class="flex flex-wrap justify-center">
    <form class="mb-4 p-4 h-40 w-full bg-white shadow rounded-lg sm:w-5/12 sm:mr-4">
      <label for="email" class="block my-1 text-sm text-gray-700 font-semibold">E-mail Address</label>
      <input id="email" bind:value={$modelStore.email} type="email" class="form-input text-gray-600 font-semibold" />
      <div class="text-right mt-6">
        <button class="btn-black capitalize hover:bg-gray-700 sm:w-auto">Change E-mail</button>
      </div>
      </form>
    <form class="p-4 w-full bg-white shadow rounded-lg sm:w-5/12">
      <label for="password" class="block my-1 text-sm text-gray-700 font-semibold">Current Password</label>
      <input id="password" type="password" class="form-input text-gray-600 font-semibold" />
      <label for="new_password" class="block my-1 text-sm text-gray-700 font-semibold">New Password</label>
      <input id="new_password" type="password" class="form-input text-gray-600 font-semibold" />
      <label for="confirm_password" class="block my-1 text-sm text-gray-700 font-semibold">Confirm New Password</label>
      <input id="confirm_password" type="password" class="form-input text-gray-600 font-semibold" />
      <div class="text-right mt-6">
        <button class="btn-black hover:bg-gray-700 sm:w-auto">Update</button>
      </div>
    </form>
  </div>
</div>
