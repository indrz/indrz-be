import { Locator, Page } from '@playwright/test';

export class LeftPaneComponent {
  private page: Page;
  sideBar: Locator;
  closeLeftPaneBtn: Locator;
  private campusLocationsHeading: Locator;
  private directionsItem: Locator;

  constructor(page: Page) {
    this.page = page;
    this.sideBar = this.page.getByTestId('sideBar');
    this.closeLeftPaneBtn = this.page.getByTestId('closeLeftPaneBtn');
    this.campusLocationsHeading = this.page.getByTestId(
      'CampusLocationsHeading'
    );
    this.directionsItem = this.page.getByTestId('directionsItem');
  }

  async closeLeftPane() {
    await this.closeLeftPaneBtn.click();
  }

  async toggleCampusLocations() {
    await this.campusLocationsHeading.click();
  }

  async showDirections() {
    await this.directionsItem.click();
  }
}
