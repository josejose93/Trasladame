<template>
  <v-container>
    <v-data-table
      :headers="headers"
      :items="destinationsFinal"
      sort-by="destinationsFinal"
      class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>Trayectos con Promedio de Pasajeros</v-toolbar-title>
          <v-divider class="mx-4" inset vertical></v-divider>
          <v-spacer></v-spacer>
        </v-toolbar>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon small class="mr-2" @click="editItem(item)"> mdi-pencil </v-icon>
        <v-icon small @click="deleteItem(item)"> mdi-delete </v-icon>
      </template>
      <template v-slot:no-data>
        <v-container>
          <h1>No se registraron Trayectos</h1>
        </v-container>
      </template>
    </v-data-table>
  </v-container>
</template>

<script>
import getAPI from "../api/busApi";

export default {
  data: () => ({
    headers: [
      {
        text: "Trayecto",
        align: "start",
        value: "destination",
      },
      { text: "Promedio de Pasajeros", value: "passenger_average" },
    ],
    destinations: [],
    destinationsFinal: [],
  }),

  computed: {},

  watch: {},

  created() {
    this.initialize();
  },

  methods: {
    getDestinations() {
      getAPI
        .get("/api/destination-passenger-average/")
        .then((response) => {
          console.log("load data");
          this.destinations = response.data.results;
          this.destinationsFinal = this.destinations.map((d) => {
            const { passenger_average } = d;
            console.log(passenger_average);
            return {
              ...d,
              passenger_average: `${passenger_average} pasajero(s)`,
            };
          });
          console.log(this.destinationsFinal);
        })
        .catch((err) => {
          console.log(err);
        });
    },

    initialize() {
      this.getDestinations();
    },
  },
};
</script>

<style>
</style>