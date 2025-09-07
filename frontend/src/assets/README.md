# Floor Changer
To change the appearance of Floor Changer, define the styles inside [floor_changer.scss](./custom_css/floor_changer.scss) file.
For example:
```scss
.floor-changer {
  position: absolute !important;
  right: 10px;
  top: 70px;
  overflow-x: hidden;
  .v-list {
    background-color: #ffffff !important;
    .v-list-item-group {
      background: transparent !important;
      .v-list-item{
        .v-list-item__title {
          color: #000000 !important;
        }
      }
      .v-list-item--active{
        background-color: #FF0000 !important;
        .v-list-item__title {
          color: #ffffff !important;
        }
      }
      .v-list-item:hover{
        cursor: pointer;
        background-color: rgba(255, 0, 0, 0.1) !important;
      }
    }
  }
}
```
