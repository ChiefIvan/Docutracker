<script lang="ts">
  import { userData } from "../../store";
  import UserDashbaord from "../lib/UserDashbaord.svelte";
  import SecretaryDashboard from "../lib/SecretaryDashboard.svelte";
  import UnverifiedComp from "../shared/UnverifiedComp.svelte";
  import CheckAuthenticity from "../shared/CheckAuthenticity.svelte";

  export let authToken: string;
</script>

<CheckAuthenticity {authToken}></CheckAuthenticity>

{#if $userData.previlage === "User"}
  <UserDashbaord {authToken} on:switch on:edit></UserDashbaord>
{:else if $userData.previlage === "Secretary"}
  <SecretaryDashboard {authToken}></SecretaryDashboard>
{:else}
  <UnverifiedComp></UnverifiedComp>
{/if}
