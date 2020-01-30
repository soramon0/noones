<script>
  import Navbar from "./components/Layout/Navbar";
  import General from "./components/General";
  import Measures from "./components/Measures";
  import Photos from "./components/Photos";
  import Settings from "./components/Settings";

  let tab = 0;

  const changeTab = ({ detail }) => {
    tab = detail;
  };
</script>

<Navbar on:changeTab={changeTab} />

{#if tab === 0}
  <General />
{:else if tab === 1}
  <Measures />
{:else if tab === 2}
  <Photos />
{:else}
  <Settings />
{/if}
