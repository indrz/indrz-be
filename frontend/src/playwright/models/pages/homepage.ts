import { Locator, Page, expect } from '@playwright/test';
import { LeftPaneComponent } from '../components/leftPaneComponent';
import { MapComponent } from '../components/mapComponent';

export class HomePage {
  private page: Page;
  searchToolbar: Locator;
  private toggleLeftPaneBtn: Locator;
  private searchInput: Locator;
  private directionsShortcutBtn: Locator;
  leftPaneComponent: LeftPaneComponent;
  mapComponent: MapComponent;

  constructor(page: Page) {
    this.page = page;
    this.searchToolbar = this.page.getByTestId('searchToolbar');
    this.toggleLeftPaneBtn = this.page.getByTestId('leftPaneToggleBtn');
    this.searchInput = this.page.getByTestId('searchInput');
    this.directionsShortcutBtn = this.page.getByTestId('directionsShortcutBtn');
    this.leftPaneComponent = new LeftPaneComponent(page);
    this.mapComponent = new MapComponent(page);
  }

  async clickToggleLeftPane() {
    await this.toggleLeftPaneBtn.click();
    await this.page.waitForTimeout(1000);
  }

  async clickDirectionsShortcut() {
    await this.directionsShortcutBtn.click();
    await this.page.waitForTimeout(1000);
  }
}
