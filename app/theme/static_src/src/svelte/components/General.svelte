<script>
  import Breadcrumb from "./shared/Breadcrumb";
  export let modelStore;

</script>

<Breadcrumb activeText="General" />

<!-- {$modelStore.first_name} -->
<div class="container mx-auto mt-4">
  <h1>{$modelStore.first_name}</h1>
</div>
