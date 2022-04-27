<template>
  <v-container>
    <v-data-table
      :headers="headers"
      :items="busesFinales"
      sort-by="license_plate"
      class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>Buses Repletos !!!</v-toolbar-title>
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
          <h1>No se registraron Buses</h1>
        </v-container>
      </template>
    </v-data-table>
  </v-container>
</template>

<script>
import getAPI from "../api/busApi";

export default {
  data: () => ({
    drivers: [],
    driversList: [],
    headers: [
      {
        text: "Placa",
        align: "start",
        value: "license_plate",
      },
      { text: "Chofer", value: "driver" },
    ],
    buses: [],
    busesFinales: [],
  }),

  computed: {},

  watch: {},

  created() {
    this.initialize();
  },

  methods: {
    getBuses() {
      getAPI
        .get("/api/buses-overflow/")
        .then((response) => {
          console.log("load data");
          this.buses = response.data;
          this.busesFinales = this.buses.map((b) => {
            const { driver } = b;
            return {
              ...b,
              driver: `${driver.first_name} ${driver.last_name}`,
            };
          });
        })
        .catch((err) => {
          console.log(err);
        });
    },

    initialize() {
      this.getBuses();
    },
  },
};
</script>

<style>
</style>