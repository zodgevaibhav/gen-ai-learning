package org.dnyanyog.service;

import java.time.LocalDate;
import org.apache.log4j.Logger;
import org.dnyanyog.dto.request.LoginRequest;
import org.dnyanyog.dto.response.LoginResponse;
import org.dnyanyog.entity.Users;
import org.dnyanyog.jwt.service.JwtUtil;
import org.dnyanyog.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class LoginService {

  @Autowired private UserRepository userRepository;

  @Autowired private JwtUtil jwtUtil;

  private static final Logger logger = Logger.getLogger(LoginService.class);
  int failedLoginAttempt;

  @Transactional
  public ResponseEntity<LoginResponse> loginUser(LoginRequest request) {

    Users userFromDb = userRepository.findByuserName(request.getUserName());

    if (request.getUserName() == null) {
      logger.info("Validation failed");
      return createErrorResponse(422, "User Name is required", "N/A");
    }

    if (request.getPassword() == null) {
      logger.info("Validation failed");
      return createErrorResponse(422, "Password is required", "N/A");
    }

    if (request.getTenant() == null) {
      logger.info("Validation failed");
      return createErrorResponse(422, "Tenant is required", "N/A");
    }

    if (userFromDb == null) {
      logger.info("Account not found");
      return createErrorResponse(404, "Account not found", "N/A");
    }

    if (!userFromDb.getUserStatus().equals("ACTIVE")) {
      if (userFromDb.getUserStatus().equals("INACTIVE")) {
        logger.info("Account is inactive");
        return createErrorResponse(403, "Account is inactive", "N/A");
      }

      if (userFromDb.getUserStatus().equals("LOCKED")) {
        logger.info("Account is locked");
        return createErrorResponse(405, "Account is locked", "N/A");
      }

      if (userFromDb.getUserStatus().equals("EXPIRED")) {
        logger.info("Password has expired");
        return createErrorResponse(402, "Password has expired", "N/A");
      }
    }

    if (!userFromDb.getPassword().equals(request.getPassword())) {
      if (userFromDb.getFailedLoginAttempts() >= 5) {
        userFromDb.setUserStatus("LOCKED");
        userFromDb.setFailedLoginAttempts(0);
        userRepository.saveAndFlush(userFromDb);
        logger.info("Account locked due to too many failed login attempts");
        return createErrorResponse(405, "Account is locked", "N/A");
      }

      int failedLoginAttempt = userFromDb.getFailedLoginAttempts() + 1;
      userFromDb.setFailedLoginAttempts(failedLoginAttempt);
      userRepository.saveAndFlush(userFromDb);
      logger.info("Invalid username or password. Failed login attempts: " + failedLoginAttempt);

      return createErrorResponse(401, "Invalid username or password", "N/A");
    }

    if (!userFromDb.getTenant().equals(request.getTenant())) {
      int failedLoginAttempt = userFromDb.getFailedLoginAttempts() + 1;
      userFromDb.setFailedLoginAttempts(failedLoginAttempt);
      userRepository.saveAndFlush(userFromDb);
      logger.info(
          "Invalid username, password or tenant. Failed login attempts: " + failedLoginAttempt);

      return createErrorResponse(
          401, "Invalid username, password or tenant. Failed login attempts:", "N/A");
    }

    userFromDb.setFailedLoginAttempts(0);
    userRepository.saveAndFlush(userFromDb);

    if (LocalDate.now().isAfter(userFromDb.getPasswordExpiryDate())) {
      userFromDb.setUserStatus("EXPIRED");
      userRepository.saveAndFlush(userFromDb);
      logger.info("Password has expired");
      return createErrorResponse(402, "Password has expired", "N/A");
    }

    return createSuccessResponse(userFromDb);
  }

  private ResponseEntity<LoginResponse> createErrorResponse(int code, String message, String role) {

    LoginResponse response = new LoginResponse();
    response.setResponseCode(code);
    response.setResponseMessage(message);
    response.setRole(role);
    return ResponseEntity.status(HttpStatus.OK).body(response);
  }

  private ResponseEntity<LoginResponse> createSuccessResponse(Users userFromDb) {

    LoginResponse response = new LoginResponse();
    response.setResponseCode(HttpStatus.OK.value());
    response.setResponseMessage("Login successful");
    response.setName(userFromDb.getName());
    response.setRole(userFromDb.getUserRole());
    response.setTenant(userFromDb.getTenant());
    response.setUserId(userFromDb.getUserId());

    HttpHeaders headers = new HttpHeaders();

    String tenantId = null == userFromDb.getTenant() ? "Dummy" : userFromDb.getTenant();
    String token =
        jwtUtil.generateToken(userFromDb.getUserName(), userFromDb.getUserRole(), tenantId);

    headers.set("Authorization", token);

    logger.info("Login successful ");

    return ResponseEntity.ok().headers(headers).body(response);
  }
}
