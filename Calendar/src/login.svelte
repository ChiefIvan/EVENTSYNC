<script>
  let email = $state("");
  let password = $state("");

  const handleLogin = async (e) => {
    e.preventDefault();

    if (email.length && email !== "codebyters.admin@dorsu.edu.ph") {
      alert("You don not have permission to access this page");
      return;
    }

    try {
      const request = await fetch(
        "https://chiefban.pythonanywhere.com/auth/login",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ email: email, psw: password }),
        }
      );

      const response = await request.json();

      if (request.ok) {
        localStorage.setItem("token", response.token);
        window.location.href = "/calendar";
      } else {
        alert(response.msg);
      }
    } catch (err) {
      console.log(err);
      // alert("Server Unreachable!");
    }
  };
</script>

<svelte:head>
  <title>EventSync | Login</title>
</svelte:head>

<main>
  <form onsubmit={handleLogin}>
    <img src="../icon.png" alt="" />
    <input type="email" placeholder="Email" bind:value={email} required />
    <input
      type="password"
      placeholder="Password"
      bind:value={password}
      required
    />
    <button>Login</button>
    {email}
  </form>
</main>

<style>
  main {
    height: 100dvh;
    display: flex;
    align-items: center;
    justify-content: center;

    form {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      row-gap: 0.5rem;
      padding: 1rem;
      box-shadow: 2px 3px 5px rgba(0, 0, 0, 0.1);
      border-radius: 1rem;

      img {
        max-width: 5rem;
      }

      input {
        border: 1px solid lightgray;
        padding: 0.5rem;
        border-radius: 0.2rem;
        width: 20rem;
      }

      button {
        width: 10rem;
        padding: 0.3rem;
        border-radius: 0.2rem;
        border: 1px solid transparent;
      }
    }
  }
</style>
