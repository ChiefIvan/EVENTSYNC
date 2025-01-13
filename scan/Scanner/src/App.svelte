<script>
  import { Html5Qrcode } from "html5-qrcode";
  import { onMount } from "svelte";

  let scanning = $state(false);
  let scanner = $state(null);

  onMount(() => {
    scanner = new Html5Qrcode("reader");
  });

  const handleStart = () => {
    scanner.start(
      { facingMode: "environment" },
      {
        fps: 10,
        qrbox: { width: 250, height: 250 },
      },
      onScanSuccess,
      onScanFailure
    );

    scanning = true;
  };

  async function handleStop() {
    await scanner.stop();
    scanning = false;
  }

  function onScanSuccess(decodedText, decodedResult) {
    alert(`Code matched = ${decodedText}`);
    console.log(decodedResult);
  }

  function onScanFailure(error) {
    console.warn(`Code scan error = ${error}`);
  }
  // let token = $state("");

  // onMount(() => {
  //   const params = new URLSearchParams(window.location.search);

  //   if (params.has("token")) {
  //     token = params.get("token");
  //   } else {
  //     token = "Token not found!";
  //   }
  // });
</script>

<div id="reader"></div>
{#if scanning}
  <button onclick={handleStop}> Start Scanning</button>
{:else}
  <button onclick={handleStart}> Start Scanning</button>
{/if}

<h1>
  <!-- Token: {token} -->
</h1>
