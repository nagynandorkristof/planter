import { defineCustomElement } from "vue";
import PrimeVue from "primevue/config";
import Aura from "@primeuix/themes/aura";

import "./style.css";
import HelloWorld from "./components/HelloWorld.ce.vue";

function define(name: string, component: any) {
  if (!customElements.get(name)) {
    customElements.define(
      name,
      defineCustomElement(component, {
        shadowRoot: false,
        configureApp(app) {
          app.use(PrimeVue, {
            theme: {
              preset: Aura,
            },
          });
        },
      })
    );
  }
}

define("hello-world", HelloWorld);
