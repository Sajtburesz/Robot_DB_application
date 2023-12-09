import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store';
import Toaster from '@meforma/vue-toaster'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faCircleArrowUp,faCircleArrowDown, faTrash, faPencil,faFloppyDisk, faXmark, faMagnifyingGlass,faCirclePlus,faBars} from '@fortawesome/free-solid-svg-icons'
import { library } from '@fortawesome/fontawesome-svg-core'
import { configureAxios } from './common/api.service';
library.add(faCircleArrowUp,faTrash,faCircleArrowDown,faPencil,faFloppyDisk,faXmark,faMagnifyingGlass,faCirclePlus,faBars)
configureAxios();
createApp(App).use(router).use(store).use(Toaster).component('font-awesome-icon', FontAwesomeIcon).mount('#app')
