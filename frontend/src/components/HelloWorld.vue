<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="12">
        <v-img
          :src="require('../assets/destacame-logo.png')"
          class="my-3 rounded-circle"
          contain
          height="200"
        />
      </v-col>

      <v-col class="mb-4">
        <h1 class="display-2 font-weight-bold mb-3">
          Bienvenido a TRASLADAME 
        </h1>

        <p class="subheading font-weight-regular">
          Plataforma para gestionar los viajes de una agencia de Buses
          <br>Encuentra el repo completo en
          <a
            href="https://github.com/josejose93/Trasladame"
            target="_blank"
          >GitHub</a>
        </p>
      </v-col>

      <v-col
        class="mb-5"
        cols="12"
      >
        <h2 class="headline font-weight-bold mb-3">
          Rutas de CRUD
        </h2>

        <v-row justify="center">
          <a
            v-for="(next, i) in CRUDLinks"
            :key="i"
            :href="next.href"
            class="subheading mx-3"
            target="_blank"
          >
            {{ next.text }}
          </a>
        </v-row>
      </v-col>

      <v-col
        class="mb-5"
        cols="12"
      >
        <h2 class="headline font-weight-bold mb-3">
          Funcionalidad Adicional
        </h2>

        <v-row justify="center">
          <a
            v-for="(link, i) in funcionalityAditional"
            :key="i"
            :href="link.href"
            class="subheading mx-3"
            target="_blank"
          >
            {{ link.text }}
          </a>
        </v-row>
      </v-col>

      <v-col
        class="mb-5"
        cols="12"
      >
        <h2 class="headline font-weight-bold mb-3">
          GRACIAS !!!
        </h2>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  export default {
    name: 'HelloWorld',

    data: () => ({
      funcionalityAditional: [
        {
          text: 'Crea tickets(pasajes) para pasajeros',
          href: 'http://localhost:8080/tickets',
        },
        {
          text: 'Lista de los trayectos junto a su promedio de pasajeros',
          href: 'http://localhost:8080/trayecto-pasajero',
        },
        {
          text: 'Filtro de todos los buses de un trayecto con más del N % de su capacidad vendida',
          href: 'http://localhost:8080/buses-llenos',
        },
      ],
      CRUDLinks: [
        {
          text: 'CRUD Pasajeros',
          href: 'http://localhost:8080/pasajeros',
        },
        {
          text: 'CRUD Choferes',
          href: 'http://localhost:8080/choferes',
        },
        {
          text: 'CRUD Trayectos',
          href: 'http://localhost:8080/trayectos',
        },
        {
          text: 'CRUD Buses',
          href: 'http://localhost:8080/buses',
        },
      ],
    }),
  }
</script>
