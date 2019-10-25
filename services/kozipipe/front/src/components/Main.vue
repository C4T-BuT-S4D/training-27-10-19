<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="dark">
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-text>
            User: {{ user === null ? "null or not null :thinking:" : user }}
          </b-nav-text>
        </b-navbar-nav>
        <b-navbar-nav class="ml-auto">
          <b-nav-item>
            <b-button variant="info" @click="copyModal = true">
              Copy Kozinak
            </b-button>
          </b-nav-item>
          <b-nav-item>
            <b-button variant="info" @click="createModal = true">
              Create Kozinak fortune
            </b-button>
          </b-nav-item>
          <b-nav-item>
            <b-button variant="danger" @click="registerModal = true">
              Register
            </b-button>
          </b-nav-item>
          <b-nav-item>
            <b-button variant="success" @click="loginModal = true">
              Login
            </b-button>
          </b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <b-modal id="modal-open" title="Error" v-model="openModal" @hidden="cancel">
      <div>
        {{ error !== null ? `Error: ${error}` : "" }}
      </div>
    </b-modal>
    <b-modal id="modal-exec" title="Exec" v-model="execModal" @hidden="cancel">
      <div>Result: {{ this.result }}</div>
      <div>
        {{ error !== null ? `Error: ${error}` : "" }}
      </div>
    </b-modal>
    <b-modal id="modal-view" title="View" v-model="viewModal" @hidden="cancel">
      <div>Name: {{ this.name }}</div>
      <div>Fortune: {{ this.fortune }}</div>
      <div>Pipe: {{ this.pipe }}</div>
      <div>Owner: {{ this.owner }}</div>
      <div>
        {{ error !== null ? `Error: ${error}` : "" }}
      </div>
    </b-modal>
    <b-modal
      id="modal-copy"
      title="Copy"
      v-model="copyModal"
      @hidden="cancel"
      @ok="copy"
    >
      <b-form>
        <b-form-group id="copy-name-group" label="Name:" label-for="copy-name">
          <b-form-input
            id="copy-name"
            v-model="name"
            required
            placeholder="Enter name"
          />
        </b-form-group>
        <b-form-group id="copy-url-group" label="Url:" label-for="copy-url">
          <b-form-input
            id="copy-url"
            v-model="url"
            required
            placeholder="Enter url"
          />
        </b-form-group>
      </b-form>
      <div>
        {{ error !== null ? `Error: ${error}` : "" }}
      </div>
    </b-modal>
    <b-modal
      id="modal-create"
      title="Create"
      v-model="createModal"
      @hidden="cancel"
      @ok="create"
    >
      <b-form>
        <b-form-group
          id="create-name-group"
          label="Name:"
          label-for="create-name"
        >
          <b-form-input
            id="create-name"
            v-model="name"
            required
            placeholder="Enter name"
          />
        </b-form-group>
        <b-form-group
          id="create-fortune-group"
          label="Fortune:"
          label-for="create-fortune"
        >
          <b-form-input
            id="create-fortune"
            v-model="fortune"
            required
            placeholder="Enter fortune"
          />
        </b-form-group>
        <b-form-group
          id="create-checksum-group"
          label="Checksum:"
          label-for="create-checksum"
        >
          <b-form-input
            id="create-checksum"
            v-model="checksum"
            required
            placeholder="Enter checksum"
          />
        </b-form-group>
        <b-form-group
          id="create-pipe-group"
          label="Pipe:"
          label-for="create-pipe"
        >
          <b-form-input
            id="create-pipe"
            v-model="pipe"
            required
            placeholder="Enter pipe"
          />
        </b-form-group>
      </b-form>
      <div>
        {{ error !== null ? `Error: ${error}` : "" }}
      </div>
    </b-modal>
    <b-modal
      id="modal-register"
      title="Register"
      v-model="registerModal"
      @hidden="cancel"
      @ok="register"
    >
      <b-form>
        <b-form-group
          id="reg-username-group"
          label="Your username:"
          label-for="reg-username"
        >
          <b-form-input
            id="reg-username"
            v-model="username"
            required
            placeholder="Enter username"
          />
        </b-form-group>
        <b-form-group
          id="reg-password-group"
          label="Your password:"
          label-for="reg-password"
        >
          <b-form-input
            id="reg-password"
            v-model="password"
            required
            placeholder="Enter password"
          />
        </b-form-group>
      </b-form>
      <div>
        {{ error !== null ? `Error: ${error}` : "" }}
      </div>
    </b-modal>
    <b-modal
      id="modal-login"
      title="Login"
      v-model="loginModal"
      @hidden="cancel"
      @ok="login"
    >
      <b-form>
        <b-form-group
          id="log-username-group"
          label="Your username:"
          label-for="log-username"
        >
          <b-form-input
            id="log-username"
            v-model="username"
            required
            placeholder="Enter username"
          />
        </b-form-group>
        <b-form-group
          id="reg-password-group"
          label="Your password:"
          label-for="reg-password"
        >
          <b-form-input
            id="reg-password"
            v-model="password"
            required
            placeholder="Enter password"
          />
        </b-form-group>
      </b-form>
      <div>
        {{ error !== null ? `Error: ${error}` : "" }}
      </div>
    </b-modal>
    <b-container class="mt-3">
      <b-card-group deck v-for="(chunk, i) in kozinaks" :key="i">
        <b-card
          v-for="(kozi, j) in chunk"
          :key="j"
          style="max-width: 20rem;"
          :title="kozi"
          :img-src="getUrl(i * 3 + j)"
          img-alt="Kozinak picture"
          img-top
          class="mb-2"
        >
          <b-button variant="success" @click="get(kozi)">
            View
          </b-button>
          <b-button variant="info" @click="exec(kozi)">
            Exec
          </b-button>
          <b-button variant="danger" @click="open(kozi)">
            Open
          </b-button>
          <b-card-text>
            {{ texts[(i * 3 + j) % 8] }}
          </b-card-text>
        </b-card>
      </b-card-group>
    </b-container>
  </div>
</template>

<script>
export default {
  data: function() {
    return {
      user: null,
      kozinaks: [],
      texts: [
        "Bed sincerity yet therefore forfeited his certainty neglected questions. Pursuit chamber as elderly amongst on. Distant however warrant farther to of. My justice wishing prudent waiting in be. Comparison age not pianoforte increasing delightful now. Insipidity sufficient dispatched any reasonably led ask. Announcing if attachment resolution sentiments admiration me on diminution.",
        "His having within saw become ask passed misery giving. Recommend questions get too fulfilled. He fact in we case miss sake. Entrance be throwing he do blessing up. Hearts warmth in genius do garden advice mr it garret. Collected preserved are middleton dependent residence but him how. Handsome weddings yet mrs you has carriage packages. Preferred joy agreement put continual elsewhere delivered now. Mrs exercise felicity had men speaking met. Rich deal mrs part led pure will but.",
        "Be at miss or each good play home they. It leave taste mr in it fancy. She son lose does fond bred gave lady get. Sir her company conduct expense bed any. Sister depend change off piqued one. Contented continued any happiness instantly objection yet her allowance. Use correct day new brought tedious. By come this been in. Kept easy or sons my it done.",
        "No depending be convinced in unfeeling he. Excellence she unaffected and too sentiments her. Rooms he doors there ye aware in by shall. Education remainder in so cordially. His remainder and own dejection daughters sportsmen. Is easy took he shed to kind.",
        "Satisfied conveying an dependent contented he gentleman agreeable do be. Warrant private blushes removed an in equally totally if. Delivered dejection necessary objection do mr prevailed. Mr feeling do chiefly cordial in do. Water timed folly right aware if oh truth. Imprudence attachment him his for sympathize. Large above be to means. Dashwood do provided stronger is. But discretion frequently sir the she instrument unaffected admiration everything.",
        "An country demesne message it. Bachelor domestic extended doubtful as concerns at. Morning prudent removal an letters by. On could my in order never it. Or excited certain sixteen it to parties colonel. Depending conveying direction has led immediate. Law gate her well bed life feet seen rent. On nature or no except it sussex.",
        "Stronger unpacked felicity to of mistaken. Fanny at wrong table ye in. Be on easily cannot innate in lasted months on. Differed and and felicity steepest mrs age outweigh. Opinions learning likewise daughter now age outweigh. Raptures stanhill my greatest mistaken or exercise he on although. Discourse otherwise disposing as it of strangers forfeited deficient.",
        "Wrote water woman of heart it total other. By in entirely securing suitable graceful at families improved. Zealously few furniture repulsive was agreeable consisted difficult. Collected breakfast estimable questions in to favourite it. Known he place worth words it as to. Spoke now noise off smart her ready."
      ],
      error: null,
      username: "",
      password: "",
      name: "",
      url: "",
      fortune: "",
      pipe: "",
      checksum: "",
      result: "",
      registerModal: false,
      loginModal: false,
      createModal: false,
      copyModal: false,
      openModal: false,
      execModal: false,
      viewModal: false
    };
  },
  methods: {
    update: async function() {
      const response = await this.$http.get("/list/");
      const kozinaks = response.data.result;
      this.kozinaks = this._.chunk(kozinaks, 3);
    },
    getUrl: function(index) {
      return `http://pomo-mondreganto.me/drive/random/kozipipe/${(index % 5) +
        1}.jpg`;
    },
    cancel: function() {
      this.error = null;
      this.username = "";
      this.password = "";
      this.name = "";
      this.url = "";
      this.fortune = "";
      this.pipe = "";
      this.checksum = "";
      this.owner = "";
      this.result = "";
    },
    register: async function(modal) {
      modal.preventDefault();
      const response = await this.$http.post("/register/", {
        username: this.username,
        password: this.password
      });
      const data = response.data;
      if (data.hasOwnProperty("error")) {
        this.error = data.error;
      } else {
        this.registerModal = false;
      }
    },
    login: async function(modal) {
      modal.preventDefault();
      const response = await this.$http.post("/login/", {
        username: this.username,
        password: this.password
      });
      const data = response.data;
      if (data.hasOwnProperty("error")) {
        this.error = data.error;
      } else {
        this.loginModal = false;
        this.user = this.username;
      }
    },
    create: async function(modal) {
      modal.preventDefault();
      if (this.pipe === "") {
        this.pipe = null;
      }
      const response = await this.$http.post("/kozi/", {
        name: this.name,
        fortune: this.fortune,
        checksum: this.checksum,
        pipe: this.pipe
      });
      const data = response.data;
      if (data.hasOwnProperty("error")) {
        this.error = data.error;
      } else {
        this.createModal = false;
        this.update();
      }
    },
    copy: async function(modal) {
      modal.preventDefault();
      const response = await this.$http.post("/copy_kozi/", {
        name: this.name,
        url: this.url
      });
      const data = response.data;
      if (data.hasOwnProperty("error")) {
        this.error = data.error;
      } else {
        this.copyModal = false;
        this.update();
      }
    },
    get: async function(fullname) {
      const response = await this.$http.get(`/kozi/${fullname}/`);
      const data = response.data;
      if (data.hasOwnProperty("error")) {
        this.error = data.error;
      } else {
        const result = data.result;
        this.name = result.name;
        this.fortune = result.fortune;
        this.owner = result.owner;
        this.pipe = null;
        if (result.hasOwnProperty("pipe")) {
          this.pipe = result.pipe;
        }
      }
      this.viewModal = true;
    },
    exec: async function(fullname) {
      const response = await this.$http.get(`/exec_kozi/${fullname}/`);
      const data = response.data;
      if (data.hasOwnProperty("error")) {
        this.error = data.error;
      } else {
        const result = data.result;
        this.result = result;
      }
      this.execModal = true;
    },
    open: async function(fullname) {
      const response = await this.$http.post(`/open_kozi/`, {
        kozi: fullname
      });
      const data = response.data;
      if (data.hasOwnProperty("error")) {
        this.error = data.error;
        this.openModal = true;
      } else {
        this.update();
      }
    }
  },
  mounted: async function() {
    this.update();
  }
};
</script>
