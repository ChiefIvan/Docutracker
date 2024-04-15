<script lang="ts">
  import {
    handleFetch,
    address,
    documents,
    userData,
    notifications,
    showMessage,
    notificationCount,
    type RequestAPI,
    type ResponseData,
  } from "../../store";
  import { navigate } from "svelte-routing";
  import { onMount } from "svelte";

  export let authToken: string;
  export let CheckAdminAuthenticityAddress = "";
  export let redirect = "";

  let navTo = redirect.length ? redirect : "/auth/login";
  const indexAddress = CheckAdminAuthenticityAddress.length
    ? CheckAdminAuthenticityAddress
    : `${address}/index`;
  const indexMethod = "GET";

  const authRequest: RequestAPI = {
    method: indexMethod,
    address: indexAddress,
  };

  async function fetchDataAndDispatch() {
    if (!authToken.length) {
      console.warn("Auth Token is empty");
      navigate(navTo);
      return;
    }

    try {
      const response: ResponseData = await handleFetch(authRequest, authToken);
      console.log(response);

      if (redirect.length) {
        if (response.error) {
          $showMessage = response;
          navigate(redirect);
        }
      }

      if (response && response.documents) {
        $documents = response.documents;
        response.documents.forEach((document) => {
          if (document.notifications && document.notifications.length) {
            document.notifications.forEach((notification) => {
              const isNotInNotifications = !$notifications.some(
                (n) => n.id === notification.id
              );
              if (isNotInNotifications) {
                $notifications = [...$notifications, notification];
              }
            });
          }
        });

        if (
          response.notificationCount !== undefined &&
          response.notificationCount < $notifications.length
        ) {
          console.log(true);
          $notificationCount =
            $notifications.length - response.notificationCount;
        }
      }

      $userData = response;
    } catch (error) {
      navigate(navTo);
      console.error(error);
    }
  }

  onMount(async () => {
    await fetchDataAndDispatch();
  });
</script>
