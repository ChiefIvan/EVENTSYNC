<!-- Calendar.svelte -->
<script>
  import { onMount } from "svelte";

  const dayNames = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  const monthNames = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];

  let events = [];
  let currentEvent = null;
  let regUsers = null;

  let now = new Date();
  let currentDay = now.getDate();
  let currentYear = now.getFullYear();
  let currentMonth = now.getMonth(); // 0-11

  $: daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
  $: firstDay = new Date(currentYear, currentMonth, 1).getDay();
  $: daysArray = Array.from(
    { length: daysInMonth },
    (_, i) => new Date(currentYear, currentMonth, i + 1)
  );
  $: dayNumbers = daysArray.map((date) => date.getDate());

  function prevMonth() {
    if (currentMonth === 0) {
      currentMonth = 11;
      currentYear -= 1;
    } else {
      currentMonth -= 1;
    }
  }

  function nextMonth() {
    if (currentMonth === 11) {
      currentMonth = 0;
      currentYear += 1;
    } else {
      currentMonth += 1;
    }
  }

  function daySelector(day) {
    const paddedDay = day < 10 ? `0${day}` : `${day}`;
    const selectedDate = `${monthNames[currentMonth]} ${paddedDay}, ${currentYear}`;
    console.log(selectedDate);

    const event = events.find((e) => e.event_date === selectedDate);

    return event || null;
  }

  onMount(async () => {
    try {
      const request = await fetch(
        "https://chiefban.pythonanywhere.com/views/get_all_event",
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );

      const response = await request.json();

      if (request.ok) {
        events = response;
        console.log(events);
        currentEvent = daySelector(currentDay);
        if (currentEvent) {
          regUsers = getRegUsers(currentEvent.id);
        }
      } else {
        window.location.href = "/";
      }
    } catch (e) {
      alert("Server Unreachable");
      console.error(`Server Unreachable: ${e}`);
      window.location.href = "/";
    }
  });

  const getRegUsers = async (eventId) => {
    try {
      const request = await fetch(
        "https://chiefban.pythonanywhere.com/views/get_all_reg_users",
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            event_id: eventId,
          }),
        }
      );

      const response = await request.json();

      if (request.ok) {
        console.log(response);
        return response;
      }
    } catch (e) {
      console.error(e);
    }
  };
</script>

<svelte:head>
  <title>EventSync | Calendar</title>
</svelte:head>

<main>
  <div class="calendar-wrapper">
    <div class="month-header">
      <button onclick={prevMonth}>←</button>
      {monthNames[currentMonth]}
      {currentYear}
      <button onclick={nextMonth}>→</button>
    </div>

    <section>
      <ul class="weekdays">
        {#each dayNames as day}
          <li>{day}</li>
        {/each}
      </ul>
    </section>

    <section>
      <ul class="days">
        {#each Array(firstDay) as _}
          <li class="empty"></li>
        {/each}
        {#each dayNumbers as day}
          <button
            class:today={day === now.getDate() &&
              currentMonth === now.getMonth() &&
              currentYear === now.getFullYear()}
            onclick={async () => {
              currentDay = day;
              currentEvent = daySelector(day);
              if (currentEvent) {
                regUsers = getRegUsers(currentEvent.id);
              }
            }}
          >
            <li>
              {day}
            </li>
          </button>
        {/each}
      </ul>
    </section>
  </div>
  <div class="events-wrapper">
    {#if !currentEvent}
      No Events on {currentDay}
    {:else}
      <h1>Event Name: {currentEvent["event_name"]}</h1>
      <p>{currentEvent["event_description"]}</p>
      from: {currentEvent["event_start_time"]} to: {currentEvent[
        "event_end_time"
      ]}

      {#if regUsers.length}
        <h3>Registered Users</h3>
        <ul>
          {#each regUsers as user}
            <li>{user.full_name}</li>
          {/each}
        </ul>
      {:else}
        <h3>There are no registered users for this event!</h3>
      {/if}
    {/if}
  </div>
</main>

<style>
  main {
    display: flex;
  }

  .calendar-wrapper,
  .events-wrapper {
    flex: 1;
    /* max-width: 600px; */
    margin: 20px;
  }
  .month-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 1.5em;
    margin-bottom: 10px;
  }
  .month-header button {
    font-size: 1em;
    padding: 0 10px;
    cursor: pointer;
    background: none;
    border: none;
  }
  .weekdays,
  .days {
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    text-align: center;
  }
  .weekdays li {
    font-weight: bold;
    padding: 5px;
    background: #f0f0f0;
  }
  .days li {
    padding: 10px;
    /* border: 1px solid #ddd; */
    display: flex;
    justify-content: center;
    align-items: center;
    height: 50px;
  }

  .days button {
    font-size: 1em;
    padding: 0 10px;
    cursor: pointer;
    background: none;
    border: none;
  }

  .days button:hover {
    background-color: #afafaf;
  }
  .empty {
    background: #f9f9f9;
  }
  .days .today {
    background-color: #ffebee;
  }
</style>
