import { Locator, Page } from '@playwright/test';

export type SearchInput = {
  searchText: string;
  searchResultId: string;
};

export type DirectionSearch = {
  fromSearch: SearchInput;
  toSearch: SearchInput;
  barrierFree?: boolean;
};

export class DirectionsComponent {
  private page: Page;
  directionsPane: Locator;
  private barrierFreeCheckbox: Locator;
  private toSearch: Locator;
  private fromSearch: Locator;
  private goButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.directionsPane = this.page.getByTestId('directionsPane');
    this.barrierFreeCheckbox = this.page.getByTestId('barrierFreeCheckbox');
    this.toSearch = this.page.getByTestId('toSearch').locator('input').first();
    this.fromSearch = this.page
      .getByTestId('fromSearch')
      .locator('input')
      .first();
    this.goButton = this.page.getByTestId('goButton');
  }

  async checkBarrierFree() {
    await this.barrierFreeCheckbox.check();
  }

  async uncheckBarrierFree() {
    await this.barrierFreeCheckbox.uncheck();
  }

  async setToSearch(input: SearchInput) {
    await this.toSearch.fill(input.searchText);
    await this.page.waitForTimeout(200);
    await this.page.getByText(input.searchResultId).first().click();
  }

  async setFromSearch(input: SearchInput) {
    await this.fromSearch.fill(input.searchText);
    await this.page.waitForTimeout(200);
    await this.page.getByText(input.searchResultId).first().click();
  }

  async clearToSearch() {
    await this.toSearch.click();
    await this.toSearch.fill('');
  }

  async clearFromSearch() {
    await this.fromSearch.click();
    await this.fromSearch.fill('');
  }

  async getDirections(search: DirectionSearch) {
    await this.clearFromSearch();
    await this.setFromSearch(search.fromSearch);
    await this.page.waitForTimeout(1000);
    await this.clearToSearch();
    await this.setToSearch(search.toSearch);

    if (search.barrierFree) {
      await this.checkBarrierFree();
    } else {
      await this.uncheckBarrierFree();
    }

    await this.goButton.click();
  }
}
