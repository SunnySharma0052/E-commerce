// JS interactions for FreshCart-style base template

document.addEventListener('DOMContentLoaded', () => {
    console.log("FreshCart base JS loaded ✅");

    // Add other interactive components here if needed
});



// DropDown Menu Account in My Account 
document.addEventListener('DOMContentLoaded', function () {
    const dropdownSubmenus = document.querySelectorAll('.dropdown-submenu');

    dropdownSubmenus.forEach(function (submenu) {
        submenu.addEventListener('mouseenter', function () {
            const subMenu = this.querySelector('.dropdown-menu');
            if (subMenu) {
                subMenu.style.display = 'block';
            }
        });
        submenu.addEventListener('mouseleave', function () {
            const subMenu = this.querySelector('.dropdown-menu');
            if (subMenu) {
                subMenu.style.display = 'none';
            }
        });
    });
});

//  Account & My account Dropend & Dropdown script 
// Enable hover on main dropdown
document.querySelectorAll('.nav-item.dropdown').forEach(function (dropdown) {
    dropdown.addEventListener('mouseenter', function () {
        let menu = dropdown.querySelector('.dropdown-menu');
        bootstrap.Dropdown.getOrCreateInstance(dropdown.querySelector('.dropdown-toggle')).show();
    });
    dropdown.addEventListener('mouseleave', function () {
        let menu = dropdown.querySelector('.dropdown-menu');
        bootstrap.Dropdown.getOrCreateInstance(dropdown.querySelector('.dropdown-toggle')).hide();
    });
});

// Enable hover on nested dropdown
document.querySelectorAll('.dropdown-menu .dropdown').forEach(function (subDropdown) {
    subDropdown.addEventListener('mouseenter', function () {
        bootstrap.Dropdown.getOrCreateInstance(subDropdown.querySelector('.dropdown-toggle')).show();
    });
    subDropdown.addEventListener('mouseleave', function () {
        bootstrap.Dropdown.getOrCreateInstance(subDropdown.querySelector('.dropdown-toggle')).hide();
    });
});

