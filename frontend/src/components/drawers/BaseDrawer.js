export default {
  name: 'BaseDrawer',
  props: {
    navigation: {
      type: Boolean,
      default: function () {
        return false;
      }
    },
    show: {
      type: Boolean,
      default: function () {
        return false;
      }
    },
    data: {
      type: Object,
      default: function () {
        return {
          name: ''
        }
      }
    },
    baseMap: {
      type: Object,
      required: false,
      default: function () {
        return {}
      }
    }
  },
  data () {
    return {
      dragHandle: null,
      drawerHeight: 0
    }
  },
  computed: {
    shouldShowDrawer: {
      get: function () {
        return this.show;
      },
      set: function (value) {
        this.$emit('update:show', value)
      }
    },
    mainDrawer: {
      get: function () {
        return this.navigation;
      },
      set: function (newValue) {
        this.$emit('update:drawer', newValue);
      }
    },
    isMobile () {
      return this.$vuetify.breakpoint.mobile;
    }
  },

  mounted () {
    this.$nextTick(() =>
      this.setHeight()
    )
    window.onresize = () => {
      this.setHeight();
    };
  },

  methods: {
    setHeight () {
      const height = this.$parent.$el.clientHeight;
      this.drawerHeight = this.isMobile ? height / 3 : height;
    },
    onTransitionEnd () {
      this.$refs.drawer.$el.style.transition = ''
    },
    startDrag (event) {
      event.preventDefault();
      this.$refs.drawer.$el.style.transition = 'none';

      const initialHeight = parseFloat(window.getComputedStyle(this.$refs.drawer.$el).height); // Ensure initialHeight is correct
      const startY = event.clientY || event.touches[0].clientY;

      const drag = (event) => {
        const currentY = event.clientY || event.touches[0].clientY;
        const deltaY = currentY - startY; // Note the flipped operands
        this.drawerHeight = initialHeight - deltaY; // Note the change here
      };

      const stopDrag = () => {
        window.removeEventListener('mousemove', drag);
        window.removeEventListener('mouseup', stopDrag);
        window.removeEventListener('touchmove', drag);
        window.removeEventListener('touchend', stopDrag);
        this.$refs.drawer.$el.style.transition = ''; // Resetting transition, if any
        this.dragHandle = null;
      };

      window.addEventListener('mousemove', drag);
      window.addEventListener('mouseup', stopDrag);
      window.addEventListener('touchmove', drag);
      window.addEventListener('touchend', stopDrag);
    }

  }
};
