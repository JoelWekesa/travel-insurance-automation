# import { test, expect } from '@playwright/test';

# test('test', async ({ page }) => {
#   await page.goto('https://oldmutual.co.ke/app/public/motor-private');
#   await page.getByTestId('comprehensive-select').getByRole('button', { name: 'Select' }).click();
#   await page.getByRole('button', { name: 'Close tooltip' }).click();
#   await page.getByRole('button', { name: 'Continue' }).click();
#   await page.locator('.input-wrapper').first().click();
#   await page.getByRole('textbox', { name: 'Fullname' }).fill('test doe');
#   await page.getByRole('textbox', { name: 'Phone' }).click();
#   await page.getByRole('textbox', { name: 'Phone' }).fill('0742587248');
#   await page.getByText('About you Fullname is').click();
#   await page.locator('omk-text-field:nth-child(4) > md-outlined-text-field > .text-field > .field > .input-wrapper').click();
#   await page.locator('omk-text-field:nth-child(4) > md-outlined-text-field > .text-field > .field > .input-wrapper').click();
#   await page.getByRole('textbox', { name: 'Email' }).fill('faith.njeri@oldmutual.com');
#   await page.getByRole('button', { name: 'Continue' }).click();
#   await page.locator('.outer-circle').first().click();
#   await page.locator('.display-value').first().click();
#   await page.getByRole('menu').getByText('DATSUN').click();
#   await page.locator('div:nth-child(6) > omk-select > .anchor-wrapper > #materialField > .display-value').click();
#   await page.locator('div:nth-child(6) > omk-select > .anchor-wrapper > .sc-omk-menu-h > #selectMenu > omk-menu-item:nth-child(2) > .sc-omk-menu-item > #item > md-item').click();
#   await page.locator('.input-wrapper').first().click();
#   await page.getByRole('spinbutton', { name: 'Year of manufacture' }).fill('2011');
#   await page.locator('omk-text-field:nth-child(8) > md-outlined-text-field > .text-field > .field > .input-wrapper').click();
#   await page.getByRole('textbox', { name: 'When would you like your' }).fill('01/01/2027');
#   await page.getByRole('spinbutton', { name: 'Value of the car' }).click();
#   await page.getByRole('spinbutton', { name: 'Value of the car' }).fill('2000000');
#   await page.locator('div:nth-child(11) > omk-select > .anchor-wrapper > #materialField > .display-value').click();
#   await page.locator('div:nth-child(11) > omk-select > .anchor-wrapper > .sc-omk-menu-h > #selectMenu > omk-menu-item:nth-child(2) > .sc-omk-menu-item > #item > md-item').click();
#   await page.getByTestId('ke-alarm-installed-0').locator('omk-radio-button').click();
#   await page.locator('#ke-tracking-installed-0 > .sc-omk-radio.hydrated > .outer-circle > .inner-circle').click();
#   await page.getByRole('button', { name: 'Continue' }).click();
#   await page.getByRole('button', { name: 'Minimize live chat window' }).click();
#   await page.getByTestId('politicalViolence').locator('#input').check();
#   await page.getByTestId('excessProtector').locator('#input').check();
#   await page.getByTestId('personalAccident').locator('#input').check();
#   await page.getByTestId('courtesyCar').locator('#input').check();
#   await page.getByRole('button', { name: 'Buy Now' }).click();
#   await page.locator('.anchor-inner-container').dblclick();
#   await page.locator('.anchor-inner-container').click();
#   await page.locator('#materialField > .hydrated > md-icon > slot').first().click();
#   await page.getByRole('textbox', { name: 'National ID' }).click();
#   await page.getByRole('textbox', { name: 'National ID' }).click();
#   await page.getByRole('textbox', { name: 'National ID' }).fill('45566574');
#   await page.getByRole('textbox', { name: 'Date of Birth' }).click();
#   await page.getByRole('textbox', { name: 'Date of Birth' }).fill('01/01/2000');
#   await page.locator('#ke-gender-type-1 > .sc-omk-radio.hydrated > .outer-circle').click();
#   await page.locator('div:nth-child(7) > omk-select > .anchor-wrapper > #materialField > .display-value').click();
#   await page.getByRole('menu').getByText('Administrative Assistant', { exact: true }).click();
#   await page.getByRole('textbox', { name: 'Postal Address' }).fill('01000');
#   await page.locator('#ke-agent-select-0 > .sc-omk-radio.hydrated > .outer-circle').click();
#   await page.locator('#ke-agent-select-1 > .sc-omk-radio.hydrated > .outer-circle > .inner-circle').click();
#   await page.getByRole('button', { name: 'Next' }).click();
#   await page.getByRole('textbox', { name: 'Vehicle registration number' }).click();
#   await page.getByRole('textbox', { name: 'Vehicle registration number' }).press('CapsLock');
#   await page.getByRole('textbox', { name: 'Vehicle registration number' }).fill('K');
#   await page.getByRole('textbox', { name: 'Vehicle registration number' }).press('CapsLock');
#   await page.getByRole('textbox', { name: 'Vehicle registration number' }).fill('KAA127k');
#   await page.getByRole('textbox', { name: 'Chassis number' }).click();
#   await page.getByRole('textbox', { name: 'Chassis number' }).fill('YU7827-282h');
#   await page.getByRole('textbox', { name: 'Engine Number' }).click();
#   await page.getByRole('textbox', { name: 'Engine Number' }).fill('TYEV2782-2276');
#   await page.locator('#ke-motor-private-vehicle-details-form').click();
#   await page.locator('.display-value').first().click();
#   await page.getByRole('menu').getByText('Diesel').click();
#   await page.locator('div:nth-child(5) > omk-select > .anchor-wrapper > #materialField > .display-value').click();
#   await page.getByRole('menu').getByText('Hatchback').click();
#   await page.getByRole('spinbutton', { name: 'Sitting capacity' }).click();
#   await page.getByRole('spinbutton', { name: 'Sitting capacity' }).fill('2');
#   await page.locator('div:nth-child(7) > omk-select > .anchor-wrapper > #materialField > .display-value').click();
#   await page.getByRole('menu').getByText('Blue', { exact: true }).click();
#   await page.getByRole('spinbutton', { name: 'Years with driving license' }).click();
#   await page.getByRole('spinbutton', { name: 'Years with driving license' }).fill('2');
#   await page.getByRole('button', { name: 'Next' }).click();
#   await page.getByRole('button', { name: 'Continue' }).click();
#   await page.locator('#upload-nationalId #button').click();
#   await page.locator('#upload-nationalId #button').setInputFiles('Birthcertificate.jpg');
#   await page.locator('omk-document-upload').filter({ hasText: 'insert_drive_fileCopy of Log' }).locator('#button').click();
#   await page.locator('omk-document-upload').filter({ hasText: 'insert_drive_fileCopy of Log' }).locator('#button').setInputFiles('Birthcertificate.jpg');
#   await page.getByRole('button').filter({ hasText: 'file_upload' }).locator('#button').click();
#   await page.getByRole('button').filter({ hasText: 'file_upload' }).locator('#button').setInputFiles('Birthcertificate.jpg');
#   await page.getByRole('button', { name: 'Continue' }).click();
#   await page.getByTestId('hasDeclinedProposal').locator('#input').check();
#   await page.getByTestId('hasIncreasedPremium').locator('#input').check();
#   await page.getByTestId('hasCancelledPolicy').locator('#input').check();
#   await page.getByTestId('hasPhysicalCondition').locator('#input').check();
#   await page.getByTestId('hasDrivingOffense').locator('#input').check();
#   await page.getByRole('button', { name: 'Continue' }).click();
#   await page.locator('.outer-circle').first().click();
#   await page.locator('#ke-childDataProcessingConsent-0 > .sc-omk-radio.hydrated > .outer-circle').click();
#   await page.getByTestId('consentForNewProductsAndServices').locator('#input').check();
#   await page.getByTestId('consentForProductsAndServicesRelatedWithMyPolicy').locator('#input').check();
#   await page.getByTestId('termsAndConditions').locator('#input').check();
#   await page.getByRole('button', { name: 'Continue' }).click();
#   await page.getByRole('button', { name: 'Process Payment' }).click();
#   await page.locator('#publicWeb iframe').contentFrame().getByTestId('mptill-nav').click();
#   await page.locator('#publicWeb iframe').contentFrame().getByTestId('card-nav').click();
#   await page.locator('#publicWeb iframe').contentFrame().getByTestId('atl_ke-nav').click();
#   await page.locator('#publicWeb iframe').contentFrame().getByTestId('card-nav').click();
#   await page.locator('#publicWeb iframe').contentFrame().getByTestId('bank_transfer-nav').click();
# });



from playwright.sync_api import sync_playwright
from datetime import datetime
import os
import traceback

SCREENSHOTS_DIR = "screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

def force_continue(page):
    page.evaluate("""
        const btn = document.querySelector('button#button');
        if (btn) {
            btn.disabled = false;
            btn.removeAttribute('disabled');
            btn.click();
        }
    """)

def snap(page, name):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    page.screenshot(path=f"{SCREENSHOTS_DIR}/{ts}_{name}.png", full_page=True)

def run_motor_comprehensive():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        step = ""
        try:
            # STEP 1 – PRODUCT
            step = "Step 1: Select Motor Comprehensive"
            print(step)

            page.goto("https://oldmutual.co.ke/app/public/motor-private", timeout=60000)
            page.wait_for_timeout(4000)

            page.get_by_test_id("comprehensive-select") \
                .get_by_role("button", name="Select").click()

            try:
                page.get_by_role("button", name="Close tooltip").click(timeout=1500)
            except:
                pass

            force_continue(page)

            # STEP 2 – ABOUT YOU
            step = "Step 2: About You"
            print(step)

            page.wait_for_timeout(2000)
            page.get_by_role("textbox", name="Fullname").fill("Test Doe")
            page.get_by_role("textbox", name="Phone").fill("0742587248")
            page.get_by_role("textbox", name="Email").fill("faith.njeri@oldmutual.com")

            force_continue(page)

            # STEP 3 – VEHICLE DETAILS
            step = "Step 3: Vehicle Details"
            print(step)

            page.wait_for_timeout(3000)

            # Vehicle type (first radio = Car)
            page.locator(".outer-circle").first.click()

            # Make – keyboard
            page.locator(".display-value").first.click()
            page.wait_for_timeout(300)
            page.keyboard.press("ArrowDown")
            page.keyboard.press("Enter")

            # Model – keyboard
            page.locator("div:nth-child(6) .display-value").click()
            page.wait_for_timeout(300)
            page.keyboard.press("ArrowDown")
            page.keyboard.press("Enter")

            page.get_by_role("spinbutton", name="Year of manufacture").fill("2011")
            page.get_by_role("textbox", name="When would you like your").fill("01/01/2027")
            page.get_by_role("spinbutton", name="Value of the car").fill("2000000")

            # Usage – keyboard
            page.locator("div:nth-child(11) .display-value").click()
            page.keyboard.press("ArrowDown")
            page.keyboard.press("Enter")

            page.get_by_test_id("ke-alarm-installed-0").locator("omk-radio-button").click()
            page.locator("#ke-tracking-installed-0 .outer-circle").click()

            snap(page, "vehicle_details")
            force_continue(page)

            # STEP 4 – ADDONS
            step = "Step 4: Add-ons"
            print(step)

            page.wait_for_timeout(2000)
            page.get_by_test_id("politicalViolence").locator("#input").check()
            page.get_by_test_id("excessProtector").locator("#input").check()
            page.get_by_test_id("personalAccident").locator("#input").check()
            page.get_by_test_id("courtesyCar").locator("#input").check()

            page.get_by_role("button", name="Buy Now").click()

            # STEP 5 – PERSONAL INFO
            step = "Step 5: Personal Info"
            print(step)

            page.wait_for_timeout(3000)

            page.get_by_role("textbox", name="National ID").fill("45566574")
            page.get_by_role("textbox", name="Date of Birth").fill("01/01/2000")
            page.locator("#ke-gender-type-1 .outer-circle").click()

            # Occupation – keyboard
            page.locator("div:nth-child(7) .display-value").click()
            page.keyboard.press("ArrowDown")
            page.keyboard.press("Enter")

            page.get_by_role("textbox", name="Postal Address").fill("01000")

            page.locator("#ke-agent-select-1 .outer-circle").click()
            page.get_by_role("button", name="Next").click()

            # STEP 6 – VEHICLE REGISTRATION
            step = "Step 6: Vehicle Registration"
            print(step)

            page.wait_for_timeout(2000)

            page.get_by_role("textbox", name="Vehicle registration number").fill("KAA127K")
            page.get_by_role("textbox", name="Chassis number").fill("YU7827-282H")
            page.get_by_role("textbox", name="Engine Number").fill("TYEV2782-2276")

            # Fuel type
            page.locator(".display-value").first.click()
            page.keyboard.press("ArrowDown")
            page.keyboard.press("Enter")

            # Body type
            page.locator("div:nth-child(5) .display-value").click()
            page.keyboard.press("ArrowDown")
            page.keyboard.press("Enter")

            page.get_by_role("spinbutton", name="Sitting capacity").fill("2")

            # Color
            page.locator("div:nth-child(7) .display-value").click()
            page.keyboard.press("ArrowDown")
            page.keyboard.press("Enter")

            page.get_by_role("spinbutton", name="Years with driving license").fill("2")
            page.get_by_role("button", name="Next").click()

            # STEP 7 – DOCUMENTS
            step = "Step 7: Documents"
            print(step)

            page.wait_for_timeout(2000)
            page.locator("#upload-nationalId input").set_input_files("Birthcertificate.jpg")
            page.locator("#upload-logBook input").set_input_files("Birthcertificate.jpg")
            page.locator("omk-document-upload input").nth(2).set_input_files("Birthcertificate.jpg")

            force_continue(page)

            # STEP 8 – DECLARATIONS
            step = "Step 8: Declarations"
            print(step)

            page.get_by_test_id("hasDeclinedProposal").locator("#input").check()
            page.get_by_test_id("hasIncreasedPremium").locator("#input").check()
            page.get_by_test_id("hasCancelledPolicy").locator("#input").check()
            page.get_by_test_id("hasPhysicalCondition").locator("#input").check()
            page.get_by_test_id("hasDrivingOffense").locator("#input").check()

            force_continue(page)

            # STEP 9 – CONSENTS
            step = "Step 9: Consents"
            print(step)

            page.locator(".outer-circle").first.click()
            page.locator("#ke-childDataProcessingConsent-0 .outer-circle").click()
            page.get_by_test_id("consentForNewProductsAndServices").locator("#input").check()
            page.get_by_test_id("consentForProductsAndServicesRelatedWithMyPolicy").locator("#input").check()
            page.get_by_test_id("termsAndConditions").locator("#input").check()

            force_continue(page)

            # STEP 10 – PAYMENT
            step = "Step 10: Payment"
            print(step)

            page.wait_for_timeout(3000)
            page.get_by_role("button", name="Process Payment").click()

            page.locator("#publicWeb iframe").content_frame.get_by_test_id("mptill-nav").click()
            page.locator("#publicWeb iframe").content_frame.get_by_test_id("card-nav").click()
            page.locator("#publicWeb iframe").content_frame.get_by_test_id("bank_transfer-nav").click()

            snap(page, "payment")

            print("✅ MOTOR COMPREHENSIVE FLOW COMPLETED")

        except Exception as e:
            snap(page, "ERROR")
            print(f"❌ FAILED at {step}")
            print(str(e))
            print(traceback.format_exc())

        finally:
            browser.close()

if __name__ == "__main__":
    run_motor_comprehensive()